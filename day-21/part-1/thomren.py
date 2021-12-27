from itertools import cycle

from tool.runners.python import SubmissionPy

N_POINTS_TO_WIN = 1000


class ThomrenSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        positions = parse_input(s)
        points = [0, 0]
        player_turn = 0
        dice = cycle(range(1, 101))
        n_rolls = 0
        while points[0] < N_POINTS_TO_WIN and points[1] < N_POINTS_TO_WIN:
            d1, d2, d3 = next(dice), next(dice), next(dice)
            n_rolls += 3
            positions[player_turn] = (
                positions[player_turn] + d1 + d2 + d3 - 1
            ) % 10 + 1
            points[player_turn] += positions[player_turn]
            player_turn = 1 - player_turn

        return n_rolls * points[player_turn]


def parse_input(s):
    l1, l2 = s.strip().splitlines()
    p1 = int(l1.split()[-1])
    p2 = int(l2.split()[-1])
    return [p1, p2]


def test_thomren():
    """
    Run `python -m pytest ./day-21/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
Player 1 starting position: 4
Player 2 starting position: 8
""".strip()
        )
        == 739785
    )
