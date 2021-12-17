import bisect
import re
from typing import Optional, Set, Tuple

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
    1035,
    1081,
    1128,
    1176,
    1225,
    1275,
    1326,
    1378,
    1431,
    1485,
    1540,
    1596,
    1653,
    1711,
    1770,
    1830,
    1891,
    1953,
    2016,
    2080,
    2145,
    2211,
    2278,
    2346,
    2415,
    2485,
    2556,
    2628,
    2701,
    2775,
    2850,
    2926,
    3003,
    3081,
    3160,
    3240,
    3321,
    3403,
    3486,
    3570,
    3655,
    3741,
    3828,
    3916,
    4005,
    4095,
    4186,
    4278,
    4371,
    4465,
    4560,
    4656,
    4753,
    4851,
    4950,
    5050,
    5151,
    5253,
    5356,
    5460,
    5565,
    5671,
    5778,
    5886,
    5995,
    6105,
    6216,
    6328,
    6441,
    6555,
    6670,
    6786,
    6903,
    7021,
    7140,
    7260,
    7381,
    7503,
    7626,
    7750,
    7875,
    8001,
    8128,
    8256,
    8385,
    8515,
    8646,
    8778,
    8911,
    9045,
    9180,
    9316,
    9453,
    9591,
    9730,
    9870,
    10011,
    10153,
    10296,
    10440,
    10585,
    10731,
    10878,
    11026,
    11175,
    11325,
    11476,
    11628,
    11781,
    11935,
    12090,
    12246,
    12403,
    12561,
    12720,
    12880,
    13041,
    13203,
    13366,
    13530,
    13695,
    13861,
    14028,
    14196,
    14365,
    14535,
    14706,
    14878,
    15051,
    15225,
    15400,
    15576,
    15753,
    15931,
    16110,
    16290,
    16471,
    16653,
    16836,
    17020,
    17205,
    17391,
    17578,
    17766,
    17955,
    18145,
    18336,
    18528,
    18721,
    18915,
    19110,
    19306,
    19503,
    19701,
    19900,
    20100,
    20301,
    20503,
    20706,
    20910,
    21115,
    21321,
    21528,
    21736,
    21945,
    22155,
    22366,
    22578,
    22791,
    23005,
    23220,
    23436,
    23653,
    23871,
    24090,
    24310,
    24531,
    24753,
    24976,
    25200,
    25425,
    25651,
    25878,
    26106,
    26335,
    26565,
    26796,
    27028,
    27261,
    27495,
    27730,
    27966,
    28203,
    28441,
    28680,
    28920,
    29161,
    29403,
    29646,
    29890,
    30135,
    30381,
    30628,
    30876,
    31125,
    31375,
    31626,
    31878,
    32131,
    32385,
    32640,
    32896,
    33153,
    33411,
    33670,
    33930,
    34191,
    34453,
    34716,
    34980,
    35245,
    35511,
    35778,
    36046,
    36315,
    36585,
    36856,
    37128,
    37401,
    37675,
    37950,
    38226,
    38503,
    38781,
    39060,
    39340,
    39621,
    39903,
    40186,
    40470,
    40755,
    41041,
    41328,
    41616,
    41905,
    42195,
    42486,
    42778,
    43071,
    43365,
    43660,
    43956,
    44253,
    44551,
]


def find_min_vx(x1: int, x2: int) -> int:
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


def reach_range_vx(ax1: int, ax2: int, vx: int) -> Tuple[Optional[int], Optional[int]]:
    x_final = vx * (vx + 1) // 2
    if x_final < ax1 or vx > ax2:
        return None, None
    min_t = vx - bisect.bisect_right(X_TARGETS, x_final - ax1) + 1
    if x_final <= ax2:
        return min_t, None
    max_t = vx - bisect.bisect_left(X_TARGETS, x_final - ax2)
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
        res = 0
        for vx in range(x2 + 1):
            min_steps, max_steps = reach_range_vx(x1, x2, vx)
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
