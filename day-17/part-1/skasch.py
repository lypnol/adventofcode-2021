import bisect
import re
from typing import Tuple

from tool.runners.python import SubmissionPy

REGEX = re.compile(r"target area: x=([-0-9]+)..([-0-9]+), y=([-0-9]+)..([-0-9]+)")
X_TARGETS = [
    0,
    1,
    3,
    6,
    10,
    15,
    21,
    28,
    36,
    45,
    55,
    66,
    78,
    91,
    105,
    120,
    136,
    153,
    171,
    190,
    210,
    231,
    253,
    276,
    300,
    325,
    351,
    378,
    406,
    435,
    465,
    496,
    528,
    561,
    595,
    630,
    666,
    703,
    741,
    780,
    820,
    861,
    903,
    946,
    990,
]


def find_vx(x1: int, x2: int) -> int:
    if x1 <= 0 <= x2:
        return 0
    if x2 < 0:
        m = -1
        x1, x2 = -x2, -x1
    else:
        m = 1
    idx1 = bisect.bisect_left(X_TARGETS, x1)
    idx2 = bisect.bisect_left(X_TARGETS, x2)
    if X_TARGETS[idx1] == x1:
        return m * idx1
    if X_TARGETS[idx2] == x2:
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
        vx = find_vx(x1, x2)
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
