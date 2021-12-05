import re
from typing import Iterable, Tuple

from tool.runners.python import SubmissionPy


def full_range(start: int, end: int) -> Iterable[int]:
    yield from range(start, end, 1 if start <= end else -1)
    yield end


REGEX = re.compile("([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)")


def iterate_points(s: str) -> Iterable[Tuple[int, int]]:
    m = REGEX.match(s)
    if m is None:
        raise ValueError(f"Invalid input {s}")
    x1, y1, x2, y2 = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
    if x1 == x2:
        yield from ((x1, y) for y in full_range(y1, y2))
    elif y1 == y2:
        yield from ((x, y1) for x in full_range(x1, x2))
    else:
        yield from zip(full_range(x1, x2), full_range(y1, y2))


def parse(s: str) -> Iterable[str]:
    for line in s.splitlines():
        if stripped_line := line.strip():
            yield stripped_line


class SkaschSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        dangerous_points = set()
        once = set()
        for line in parse(s):
            for point in iterate_points(line):
                if point not in once:
                    once.add(point)
                elif point not in dangerous_points:
                    dangerous_points.add(point)
        return len(dangerous_points)


def test_skasch():
    """
    Run `python -m pytest ./day-05/part-1/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""".strip()
        )
        == 12
    )
