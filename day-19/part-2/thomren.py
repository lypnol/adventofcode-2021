from itertools import product
from typing import DefaultDict, Dict, List, Tuple

import numpy as np
import numpy.typing as npt
from scipy.spatial.distance import pdist, squareform
from scipy.spatial.transform import Rotation

from tool.runners.python import SubmissionPy

N_OVERLAP = 12

NDArrayInt = npt.NDArray[np.int_]


class ThomrenSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        beacons_per_scanner = parse_input(s)

        # affine transforms relative to scanner 0
        transforms = find_transforms(beacons_per_scanner)

        # points with positions relative to scanner 0
        all_points = {tuple(p) for p in beacons_per_scanner[0]}
        for i, ht in transforms.items():
            transformed_points = np.rint(
                apply_affine_transform(beacons_per_scanner[i], ht)
            ).astype(int)
            all_points |= {tuple(p) for p in transformed_points}

        max_dist = -1
        for (i, j) in product(range(len(beacons_per_scanner)), repeat=2):
            ti = transforms[i][:-1, -1]
            tj = transforms[j][:-1, -1]
            d = manhattan_dist(ti, tj)
            if d > max_dist:
                max_dist = d
        return round(max_dist)


def parse_input(s: str) -> List[NDArrayInt]:
    res = []
    for scanner_data in s.split("\n\n"):
        beacons = []
        for line in scanner_data.splitlines()[1:]:
            x, y, z = line.split(",")
            beacons.append((int(x), int(y), int(z)))
        res.append(np.array(beacons, dtype=int))
    return res


def find_transforms(
    beacons_per_scanner: List[NDArrayInt],
) -> Dict[int, NDArrayInt]:
    pairwise_distances = [
        pdist(np.array(sb), metric="sqeuclidean").astype(int)
        for sb in beacons_per_scanner
    ]
    possible_matches_dict = find_possible_matches(pairwise_distances)

    # affine transforms relative to scanner 0
    transforms = dict()
    transforms[0] = np.eye(4, dtype=int)

    # iteratively fill transforms
    frontier = {0}
    while len(frontier):
        i = frontier.pop()
        for j in possible_matches_dict[i]:
            if j in transforms:
                continue

            cp = find_common_points(
                beacons_per_scanner[i],
                beacons_per_scanner[j],
                pairwise_distances[i],
                pairwise_distances[j],
            )
            if cp is None:
                # False positive, no overlap despite enough similar pairwise distances
                continue
            i_common_points, j_common_points = cp

            i_centroid = np.mean(i_common_points, axis=0)
            j_centroid = np.mean(j_common_points, axis=0)

            i_centered = i_common_points - i_centroid
            j_centered = j_common_points - j_centroid

            rot, rmsd = Rotation.align_vectors(i_centered, j_centered)
            if rmsd > 1e-4:
                # False positive, points cannot be matched
                continue
            R = rot.as_matrix()
            t = i_centroid - j_centroid.T @ R.T
            ht = get_affine_transform(R, t)

            if j not in transforms:
                frontier |= {j}
            ht0 = transforms[i]
            transforms[j] = ht0 @ ht

    return transforms


def find_possible_matches(
    pairwise_distances: List[NDArrayInt],
) -> Dict[int, List[int]]:
    """Use the fact that affine transforms preserve distances between points to find
    scanners with possible overlaps of at least 12 points. If there is an overlap, then
    the pairwise distances between the overlapping points exists for both scanners."""
    N = len(pairwise_distances)
    n_similar_pairwise_distances = np.zeros((N, N), dtype=int)
    for i in range(N):
        for j in range(i + 1, N):
            pdi = pairwise_distances[i]
            pdj = pairwise_distances[j]
            n_similar_pairwise_distances[i, j] = len(set(pdi) & set(pdj))

    possible_matches_list = np.argwhere(
        n_similar_pairwise_distances >= (N_OVERLAP * (N_OVERLAP - 1) // 2)
    )

    possible_matches_dict = DefaultDict(list)
    for i, j in possible_matches_list:
        possible_matches_dict[i].append(j)
        possible_matches_dict[j].append(i)

    return possible_matches_dict


def find_common_points(
    points_i: NDArrayInt,
    points_j: NDArrayInt,
    pairwise_distances_i: NDArrayInt,
    pairwise_distances_j: NDArrayInt,
) -> Tuple[NDArrayInt, NDArrayInt]:
    i_common_indices = []
    for idx, line in enumerate(squareform(pairwise_distances_i)):
        if len(set(line) & set(pairwise_distances_j)) >= 11:
            i_common_indices.append(idx)

    j_common_indices = []
    for idx, line in enumerate(squareform(pairwise_distances_j)):
        if len(set(line) & set(pairwise_distances_i)) >= 11:
            j_common_indices.append(idx)

    if len(i_common_indices) < N_OVERLAP or len(j_common_indices) < N_OVERLAP:
        # False positive, not enough overlap despite enough similar pairwise distances
        return None

    # TODO: make it work when some points have similar pairwise distance values
    i_common_indices_sorted = np.argsort(
        np.sum(
            squareform(pairwise_distances_i)[i_common_indices, :][:, i_common_indices],
            axis=1,
        )
    )
    j_common_indices_sorted = np.argsort(
        np.sum(
            squareform(pairwise_distances_j)[j_common_indices, :][:, j_common_indices],
            axis=1,
        )
    )

    i_common_points = points_i[i_common_indices][i_common_indices_sorted]
    j_common_points = points_j[j_common_indices][j_common_indices_sorted]

    return i_common_points, j_common_points


def get_affine_transform(R, t):
    ht = np.zeros((4, 4))
    ht[:-1, :-1] = R
    ht[0:-1, -1] = t
    ht[-1, -1] = 1
    return ht


def apply_affine_transform(X, ht):
    X = np.c_[X, np.ones(len(X))]
    Y = X @ ht.T
    return Y[:, :-1]


def manhattan_dist(x, y):
    return np.abs(x - y).sum()


def test_thomren():
    """
    Run `python -m pytest ./day-19/part-2/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
""".strip()
        )
        == 3621
    )
