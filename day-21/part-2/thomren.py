from itertools import product
from functools import lru_cache
from typing import Tuple

from tool.runners.python import SubmissionPy

N_POINTS_TO_WIN = 21


class ThomrenSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        positions = parse_input(s)
        return max(solve_dirac_dice(tuple(positions), (0, 0), 0))


@lru_cache(None)
def solve_dirac_dice(
    positions: Tuple[int, int], points: Tuple[int, int], turn: int
) -> Tuple[int, int]:
    if points[0] >= N_POINTS_TO_WIN:
        return (1, 0)
    elif points[1] >= N_POINTS_TO_WIN:
        return (0, 1)

    res = (0, 0)
    for d1, d2, d3 in product(range(1, 4), repeat=3):
        new_pos = (positions[turn] + d1 + d2 + d3 - 1) % 10 + 1
        new_points = points[turn] + new_pos
        next_positions = (
            (new_pos, positions[1]) if turn == 0 else (positions[0], new_pos)
        )
        next_points = (new_points, points[1]) if turn == 0 else (points[0], new_points)
        win1, win2 = solve_dirac_dice(next_positions, next_points, 1 - turn)
        res = (res[0] + win1, res[1] + win2)
    return res


def parse_input(s):
    l1, l2 = s.strip().splitlines()
    p1 = int(l1.split()[-1])
    p2 = int(l2.split()[-1])
    return [p1, p2]


def test_thomren():
    """
    Run `python -m pytest ./day-21/part-2/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
Player 1 starting position: 4
Player 2 starting position: 8
""".strip()
        )
        == 444356092776315
    )
