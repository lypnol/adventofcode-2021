from dataclasses import dataclass
from typing import Iterable, List, Set, Tuple

from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        dots, folds = parse(s)
        dots = fold(dots, folds[0])
        return len(dots)


@dataclass(frozen=True)
class Fold:
    axis: int
    value: int


Dot = Tuple[int, int]


def parse(s: str) -> Tuple[List[Dot], List[Fold]]:
    dots_str, folds_str = s.split("\n\n")

    dots = []
    for line in dots_str.splitlines():
        x, y = line.split(",")
        dots.append((int(x), int(y)))

    folds = []
    for line in folds_str.splitlines():
        axis, value = line.split()[-1].split("=")
        folds.append(Fold(0 if axis == "x" else 1, int(value)))

    return dots, folds


def fold(dots: Iterable[Dot], fold: Fold) -> Set[Dot]:
    if fold.axis == 1:
        return {
            (x, y - 2 * (y - fold.value) if y > fold.value else y) for (x, y) in dots
        }
    else:
        return {
            (x - 2 * (x - fold.value) if x > fold.value else x, y) for (x, y) in dots
        }


def test_thomren():
    """
    Run `python -m pytest ./day-13/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
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
