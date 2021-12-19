import itertools
from typing import List, Optional, Set, Tuple, cast

import numpy as np
import numpy.typing as npt
from tool.runners.python import SubmissionPy

Array = npt.NDArray[np.int_]
Tensor = Tuple[Array, Array]

ORIENTATIONS = [
    np.array(
        [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ]
    ),
    np.array(
        [
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, -1],
        ]
    ),
    np.array(
        [
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, -1],
        ]
    ),
    np.array(
        [
            [-1, 0, 0],
            [0, -1, 0],
            [0, 0, 1],
        ]
    ),
    np.array(
        [
            [1, 0, 0],
            [0, 0, -1],
            [0, 1, 0],
        ]
    ),
    np.array(
        [
            [1, 0, 0],
            [0, 0, 1],
            [0, -1, 0],
        ]
    ),
    np.array(
        [
            [-1, 0, 0],
            [0, 0, 1],
            [0, 1, 0],
        ]
    ),
    np.array(
        [
            [-1, 0, 0],
            [0, 0, -1],
            [0, -1, 0],
        ]
    ),
    np.array(
        [
            [0, 0, 1],
            [0, 1, 0],
            [-1, 0, 0],
        ]
    ),
    np.array(
        [
            [0, 0, 1],
            [0, -1, 0],
            [1, 0, 0],
        ]
    ),
    np.array(
        [
            [0, 0, -1],
            [0, 1, 0],
            [1, 0, 0],
        ]
    ),
    np.array(
        [
            [0, 0, -1],
            [0, -1, 0],
            [-1, 0, 0],
        ]
    ),
    np.array(
        [
            [0, -1, 0],
            [1, 0, 0],
            [0, 0, 1],
        ]
    ),
    np.array(
        [
            [0, 1, 0],
            [-1, 0, 0],
            [0, 0, 1],
        ]
    ),
    np.array(
        [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, -1],
        ]
    ),
    np.array(
        [
            [0, -1, 0],
            [-1, 0, 0],
            [0, 0, -1],
        ]
    ),
    np.array(
        [
            [0, 0, 1],
            [1, 0, 0],
            [0, 1, 0],
        ]
    ),
    np.array(
        [
            [0, 0, 1],
            [-1, 0, 0],
            [0, -1, 0],
        ]
    ),
    np.array(
        [
            [0, 0, -1],
            [-1, 0, 0],
            [0, 1, 0],
        ]
    ),
    np.array(
        [
            [0, 0, -1],
            [1, 0, 0],
            [0, -1, 0],
        ]
    ),
    np.array(
        [
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 0],
        ]
    ),
    np.array(
        [
            [0, -1, 0],
            [0, 0, 1],
            [-1, 0, 0],
        ]
    ),
    np.array(
        [
            [0, 1, 0],
            [0, 0, -1],
            [-1, 0, 0],
        ]
    ),
    np.array(
        [
            [0, -1, 0],
            [0, 0, -1],
            [1, 0, 0],
        ]
    ),
]

DISTANCE = 1000
MIN_MATCHES = 8


def is_visible(
    pos0: int, pos1: int, pos2: int, beacon0: int, beacon1: int, beacon2: int
) -> bool:
    return (
        -DISTANCE <= pos0 - beacon0 <= DISTANCE
        and -DISTANCE <= pos1 - beacon1 <= DISTANCE
        and -DISTANCE <= pos2 - beacon2 <= DISTANCE
    )


def absolute(t: Tensor, scanner: Array) -> Array:
    pos, rot = t
    return scanner @ rot + pos


def find_overlap(
    t1: Tensor,
    scanner1: Array,
    scanner2: Array,
) -> Optional[Tensor]:
    pos1, _ = t1
    pos10, pos11, pos12 = pos1[0], pos1[1], pos1[2]
    abs1 = list(absolute(t1, scanner1))
    abs1set: Set[Tuple[int, int, int]] = {
        (beacon[0], beacon[1], beacon[2]) for beacon in abs1  # type: ignore
    }
    for idx2, b in enumerate(scanner2):
        for beacon1 in abs1:
            toofar = set()
            for rot2 in ORIENTATIONS:
                beacon2rel = b @ rot2
                pos2 = beacon1 - beacon2rel
                t2 = pos2, rot2
                found = 1
                for idx, beacon2 in enumerate(absolute(t2, scanner2)):
                    if idx == idx2:
                        continue
                    if idx in toofar:
                        continue
                    if not is_visible(
                        pos10, pos11, pos12, beacon2[0], beacon2[1], beacon2[2]
                    ):
                        toofar.add(idx)
                        continue
                    if (beacon2[0], beacon2[1], beacon2[2]) not in abs1set:
                        break
                    found += 1
                    if found >= MIN_MATCHES:
                        return t2
    return None


def parse(s: str) -> List[Array]:
    scanners: List[Array] = []
    beacons: List[Array] = []
    for line in s.splitlines():
        if stripped_line := line.strip():
            if stripped_line.startswith("---"):
                scanners.append(np.array(beacons))
                beacons = []
            else:
                pos = stripped_line.split(",")
                beacons.append(np.array([int(pos[0]), int(pos[1]), int(pos[2])]))
    scanners.append(np.array(beacons))
    return scanners[1:]


def find_tensors(scanners: List[Array]) -> List[Tensor]:
    tensors: List[Optional[Tensor]] = [None] * len(scanners)
    tensors[0] = (np.array([0, 0, 0]), ORIENTATIONS[0])
    found = [0]
    remaining = set(range(1, len(scanners)))
    compared = set()
    while remaining:
        idx2: Optional[int] = None
        for idx1 in found:
            t1 = tensors[idx1]
            t2 = None
            assert t1 is not None
            scanner1 = scanners[idx1]
            for idx2 in remaining:
                if tuple(sorted([idx1, idx2])) in compared:
                    continue
                compared.add(tuple(sorted([idx1, idx2])))
                scanner2 = scanners[idx2]
                t2 = find_overlap(t1, scanner1, scanner2)
                if t2 is not None:
                    break
            if t2 is not None:
                assert idx2 is not None
                break
        else:
            raise RuntimeError
        # print(idx2)
        assert t2 is not None
        assert idx2 is not None
        tensors[idx2] = t2
        remaining.remove(idx2)
        found.append(idx2)
    return cast(List[Tensor], tensors)


class SkaschSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        scanners = parse(s)
        tensors = find_tensors(scanners)
        max_dist = 0
        for (pos1, _), (pos2, _) in itertools.combinations(tensors, 2):
            max_dist = max(max_dist, abs(pos1 - pos2).sum())
        return max_dist


def test_skasch() -> None:
    """
    Run `python -m pytest ./day-19/part-2/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
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
