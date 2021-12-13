import re
from typing import Callable, List, Tuple
from tool.runners.python import SubmissionPy


FOLD_REGEX = re.compile(r"fold along (x|y)=([0-9]+)")


def parse(s: str) -> Tuple[List[Tuple[int, int]], List[Tuple[bool, int]]]:
    points = []
    folds = []
    fill_folds = False
    for line in s.splitlines():
        line = line.strip()
        if fill_folds:
            m = FOLD_REGEX.match(line)
            assert m is not None
            folds.append((m.group(1) == "x", int(m.group(2))))
        elif not line:
            fill_folds = True
        else:
            point = line.split(",")
            points.append((int(point[1]), int(point[0])))
    return points, folds


def fold_to_op(fold: Tuple[bool, int]) -> Callable[[Tuple[int, int]], Tuple[int, int]]:
    x_axis, pos = fold
    if x_axis:
        return lambda p: (p[0], min(p[1], 2 * pos - p[1]))
    else:
        return lambda p: (min(p[0], 2 * pos - p[0]), p[1])


class SkaschSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        points, folds = parse(s)
        op = fold_to_op(folds[0])
        pts = {op(point) for point in points}
        return len(pts)


def test_skasch() -> None:
    """
    Run `python -m pytest ./day-13/part-1/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""".strip()
        )
        == 17
    )
