from itertools import product
from typing import DefaultDict

import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.spatial.transform import Rotation

from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        scan_beacons = parse_input(s)
        pairwise_distances = [
            pdist(np.array(sb), metric="sqeuclidean").astype(int) for sb in scan_beacons
        ]

        n_possible_matches = np.zeros((len(scan_beacons), len(scan_beacons)), dtype=int)
        for i in range(len(scan_beacons)):
            for j in range(i + 1, len(scan_beacons)):
                pdi = pairwise_distances[i]
                pdj = pairwise_distances[j]
                n_possible_matches[i, j] = len(set(pdi) & set(pdj))

        possible_matches = np.argwhere(n_possible_matches >= (12 * 11 // 2))

        possible_matches_dict = DefaultDict(list)
        for i, j in possible_matches:
            possible_matches_dict[i].append(j)
            possible_matches_dict[j].append(i)

        all_points = {tuple(p) for p in scan_beacons[0]}
        transforms = dict()
        transforms[0] = np.eye(4, dtype=int)
        frontier = {0}
        while len(frontier):
            i = frontier.pop()
            for j in possible_matches_dict[i]:
                if j in transforms:
                    continue
                pdi = pairwise_distances[i]
                pdj = pairwise_distances[j]

                i_common = []
                for idx, line in enumerate(squareform(pdi)):
                    if len(set(line) & set(pdj)) >= 11:
                        i_common.append(idx)
                j_common = []
                for idx, line in enumerate(squareform(pdj)):
                    if len(set(line) & set(pdi)) >= 11:
                        j_common.append(idx)

                i_common_sorted = np.argsort(
                    np.sum(squareform(pdi)[i_common, :][:, i_common], axis=1)
                )
                j_common_sorted = np.argsort(
                    np.sum(squareform(pdj)[j_common, :][:, j_common], axis=1)
                )

                i_common_points = np.array(scan_beacons[i], dtype=int)[i_common][
                    i_common_sorted
                ]
                j_common_points = np.array(scan_beacons[j], dtype=int)[j_common][
                    j_common_sorted
                ]

                i_centroid = np.mean(i_common_points, axis=0)
                j_centroid = np.mean(j_common_points, axis=0)
                i_centered = i_common_points - i_centroid
                j_centered = j_common_points - j_centroid
                rot, rmsd = Rotation.align_vectors(i_centered, j_centered)
                R = rot.as_matrix()
                t = i_centroid - j_centroid.T @ R.T
                ht = get_affine_transform(R, t)
                if rmsd > 1e-4:
                    # false positive, points cannot be matched
                    continue

                ht0 = transforms[i]
                if j not in transforms:
                    frontier |= {j}
                transforms[j] = ht0 @ ht

                sbj = np.array(scan_beacons[j], dtype=int)
                transformed_points = np.rint(
                    apply_affine_transform(sbj, transforms[j])
                ).astype(int)
                all_points |= {tuple(p) for p in transformed_points}

        m = -1
        for (i, j) in product(range(len(scan_beacons)), repeat=2):
            ti = transforms[i][:-1, -1]
            tj = transforms[j][:-1, -1]
            d = manhattan_dist(ti, tj)
            if d > m:
                m = d
        return round(m)


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


def parse_input(s):
    res = []
    for scanner_data in s.split("\n\n"):
        beacons = []
        for line in scanner_data.splitlines()[1:]:
            x, y, z = line.split(",")
            beacons.append((int(x), int(y), int(z)))
        res.append(beacons)
    return res


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
