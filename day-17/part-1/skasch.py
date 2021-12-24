import bisect
import re
from typing import List, Tuple

from tool.runners.python import SubmissionPy

REGEX = re.compile(r"target area: x=([-0-9]+)..([-0-9]+), y=([-0-9]+)..([-0-9]+)")


def find_vx(x1: int, x2: int, x_targets: List[int]) -> int:
    if x1 <= 0 <= x2:
        return 0
    if x2 < 0:
        m = -1
        x1, x2 = -x2, -x1
    else:
        m = 1
    idx1 = bisect.bisect_left(x_targets, x1)
    idx2 = bisect.bisect_left(x_targets, x2)
    if x_targets[idx1] == x1:
        return m * idx1
    if x_targets[idx2] == x2:
        return m * idx1
    if idx1 == idx2:
        raise ValueError
    return m * idx1


def find_vy(y1: int, y2: int) -> Tuple[int, bool]:
    vy1 = y1 if y1 >= 0 else -y1 - 1
    vy2 = y2 if y2 >= 0 else -y2 - 1
    if vy1 > vy2:
        return vy1, y1 >= 0
    return vy2, y2 >= 0


def parse(s: str) -> Tuple[int, int, int, int]:
    m = REGEX.match(s.strip())
    if m is not None:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))
    raise ValueError


class SkaschSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        x1, x2, y1, y2 = parse(s)
        x_targets = [n * (n + 1) // 2 for n in range(max(-x1, x2) + 1)]
        vx = find_vx(x1, x2, x_targets)
        vy, pos = find_vy(y1, y2)
        assert vx <= vy + (-1 if pos else 1)
        return (vy * (vy + 1)) // 2


def test_skasch() -> None:
    """
    Run `python -m pytest ./day-17/part-1/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
target area: x=20..30, y=-10..-5
""".strip()
        )
        == 45
    )
