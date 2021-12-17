import bisect
import re
from typing import List, Optional, Set, Tuple

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


def reach_range_vx(
    ax1: int, ax2: int, vx: int, x_targets: List[int]
) -> Tuple[Optional[int], Optional[int]]:
    x_final = vx * (vx + 1) // 2
    if x_final < ax1 or vx > ax2:
        return None, None
    min_t = vx - bisect.bisect_right(x_targets, x_final - ax1) + 1
    if x_final <= ax2:
        return min_t, None
    max_t = vx - bisect.bisect_left(x_targets, x_final - ax2)
    if max_t < min_t:
        return None, None
    return min_t, max_t


def reach_range_y_in(y1: int, y2: int, steps: int) -> Set[int]:
    max_vy = (y2 + steps * (steps - 1) // 2) // steps
    min_vy = (y1 + steps * (steps - 1) // 2 + steps - 1) // steps
    return {vy for vy in range(min_vy, max_vy + 1)}


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
        assert x1 * x2 >= 0
        if x2 <= 0:
            x1, x2 = -x2, -x1
        x_targets = [n * (n + 1) // 2 for n in range(x2 + 1)]
        res = 0
        min_vx = find_vx(x1, x2, x_targets)
        for vx in range(min_vx, x2 + 1):
            min_steps, max_steps = reach_range_vx(x1, x2, vx, x_targets)
            if min_steps is None:
                continue
            if max_steps is None:
                max_vy, _ = find_vy(y1, y2)
                max_steps = max_vy * 2 + 2
            vys = set()
            for steps in range(min_steps, max_steps + 1):
                vys |= reach_range_y_in(y1, y2, steps)
            res += len(vys)
        return res


def test_skasch() -> None:
    """
    Run `python -m pytest ./day-17/part-2/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
target area: x=20..30, y=-10..-5
""".strip()
        )
        == 112
    )
