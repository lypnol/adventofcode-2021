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
        for f in folds:
            dots = fold(dots, f)
        return pformat_dots(dots)


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


def pformat_dots(dots: Iterable[Dot]) -> str:
    xmax, ymax = max(d[0] for d in dots), max(d[1] for d in dots)
    return "\n".join(
        "".join("#" if (x, y) in dots else "." for x in range(xmax + 2))
        for y in range(ymax + 1)
    )
