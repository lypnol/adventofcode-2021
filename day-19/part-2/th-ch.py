from tool.runners.python import SubmissionPy

from collections import deque
from itertools import product, permutations


def compute_orientations(beacon, include_all=False):
    oriented_coords = []
    x, y, z = beacon
    for i in range(3):  # fixed axis
        base = [x, y, z]
        for _ in range(4):
            base[i], base[i - 1] = base[i - 1], -base[i]
            for _ in range(4):  # rotations
                base[i - 1], base[i - 2] = -base[i - 2], base[i - 1]
                if include_all or tuple(base[:]) not in oriented_coords:
                    oriented_coords.append(tuple(base[:]))

        base = [x, y, z]
        for _ in range(4):
            base[i], base[i - 2] = base[i - 2], -base[i]
            for _ in range(4):  # rotations
                base[i - 1], base[i - 2] = -base[i - 2], base[i - 1]
                if include_all or tuple(base[:]) not in oriented_coords:
                    oriented_coords.append(tuple(base[:]))

    return oriented_coords


def compute_vectors(beacons):
    starting_point_by_vector = {}
    for i, j in permutations(range(len(beacons)), 2):
        vector = (
            beacons[i][0] - beacons[j][0],
            beacons[i][1] - beacons[j][1],
            beacons[i][2] - beacons[j][2],
        )
        starting_point_by_vector[vector] = beacons[i]

    return starting_point_by_vector


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        beacons_by_scanner = {}

        for scanner in s.split("\n\n"):
            lines = scanner.splitlines()
            scanner_nb = int(lines[0].replace("--- scanner ",
                                              "").replace(" ---", ""))
            beacons = []
            for line in lines[1:]:
                coords = line.split(",")
                beacons.append(tuple(int(x) for x in coords))

            beacons_by_scanner[scanner_nb] = []
            for orientation in zip(*[
                    compute_orientations(beacon, include_all=False)
                    for beacon in beacons
            ]):
                beacons_by_scanner[scanner_nb].append(sorted(orientation))

        scanners_to_process = deque(beacons_by_scanner.keys())
        identified_scanners = set()
        position_by_scanner = {0: (0, 0, 0)}
        final_beacons = set()

        while scanners_to_process:
            s1 = scanners_to_process.popleft()
            has_identified = False
            for s2 in scanners_to_process:
                if s1 in identified_scanners and s2 in identified_scanners:
                    continue

                nb_orientations = max(len(beacons_by_scanner[s2]),
                                      len(beacons_by_scanner[s1]))
                for i, j in product(range(nb_orientations), repeat=2):
                    if i >= len(beacons_by_scanner[s2]) or j >= len(
                            beacons_by_scanner[s1]):
                        continue

                    starting_point_by_vector1 = compute_vectors(
                        beacons_by_scanner[s1][j])
                    starting_point_by_vector2 = compute_vectors(
                        beacons_by_scanner[s2][i])

                    inter = set(starting_point_by_vector2.keys()).intersection(
                        starting_point_by_vector1.keys())

                    if len(inter) >= 11:
                        # restrict orientations
                        beacons_by_scanner[s1] = [beacons_by_scanner[s1][j]]
                        beacons_by_scanner[s2] = [beacons_by_scanner[s2][i]]
                        # Mark scanner as identified
                        identified_scanners.add(s1)
                        identified_scanners.add(s2)
                        has_identified = True
                        break

                if has_identified:
                    # compute scanner position
                    vector = inter.pop()
                    point1 = starting_point_by_vector1[vector]
                    point2 = starting_point_by_vector2[vector]

                    if s1 in position_by_scanner:
                        position_by_scanner[s2] = tuple(
                            position_by_scanner[s1][k] + point1[k] - point2[k]
                            for k in range(3))
                    if s2 in position_by_scanner:
                        position_by_scanner[s1] = tuple(
                            position_by_scanner[s2][k] + point2[k] - point1[k]
                            for k in range(3))

                    break

            if has_identified:
                # Re-enqueue scanners to find more pairs
                scanners_to_process.appendleft(s2)
                scanners_to_process.appendleft(s1)
                for ss in [s1, s2]:
                    for beacon in beacons_by_scanner[ss][0]:
                        absolute_beacon = tuple(beacon[k] +
                                                position_by_scanner[ss][k]
                                                for k in range(3))
                        final_beacons.add(absolute_beacon)

        max_distance = -1
        for s1, s2 in permutations(position_by_scanner.keys(), 2):
            dist = sum(
                abs(position_by_scanner[s2][k] - position_by_scanner[s1][k])
                for k in range(3))
            max_distance = max(max_distance, dist)

        return max_distance


def test_th_ch():
    """
    Run `python -m pytest ./day-19/part-1/th-ch.py` to test the submission.
    """
    assert (ThChSubmission().run("""
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
""".strip()) == 3621)
