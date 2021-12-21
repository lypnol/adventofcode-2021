import collections
import functools
import re
from typing import DefaultDict, List, Tuple
from tool.runners.python import SubmissionPy

REGEX = re.compile(r"Player [1-2] starting position: ([0-9]+)")


def parse(s: str) -> List[int]:
    vs: List[int] = []
    for line in s.splitlines():
        if stripped_line := line.strip():
            m = REGEX.match(stripped_line)
            assert m is not None
            vs.append(int(m.group(1)))
    return vs


BOARD_SIZE = 10
MAX_SCORE = 21


@functools.lru_cache(None)
def move(pos_min1: int, throw: int) -> int:
    return (pos_min1 + throw) % BOARD_SIZE + 1


DIRAC_DICE = [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]


class SkaschSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        pos1, pos2 = parse(s)
        states: DefaultDict[Tuple[int, int, int, int], int] = collections.defaultdict(int)
        won = [0, 0]
        states[pos1 - 1, pos2 - 1, 0, 0] = 1
        valid_states = {(pos1 - 1, pos2 - 1, 0, 0)}
        player = 0
        while valid_states:
            new_valid_states = set()
            new_states: DefaultDict[Tuple[int, int, int, int], int] = collections.defaultdict(int)
            for pos1_min1, pos2_min1, score1, score2 in valid_states:
                count = states[pos1_min1, pos2_min1, score1, score2]
                for throw, n_throws in DIRAC_DICE:
                    if player == 0:
                        new_pos1 = move(pos1_min1, throw)
                        new_score1 = score1 + new_pos1
                        if new_score1 >= MAX_SCORE:
                            won[player] += n_throws * count
                        else:
                            new_states[new_pos1 - 1, pos2_min1, new_score1, score2] += n_throws * count
                            new_valid_states.add((new_pos1 - 1, pos2_min1, new_score1, score2))
                    else:
                        new_pos2 = move(pos2_min1, throw)
                        new_score2 = score2 + new_pos2
                        if new_score2 >= MAX_SCORE:
                            won[player] += n_throws * count
                        else:
                            new_states[pos1_min1, new_pos2 - 1, score1, new_score2] += n_throws * count
                            new_valid_states.add((pos1_min1, new_pos2 - 1, score1, new_score2))
            player = 1 - player
            states = new_states
            valid_states = new_valid_states
        return max(won)


def test_skasch() -> None:
    """
    Run `python -m pytest ./day-21/part-2/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
Player 1 starting position: 4
Player 2 starting position: 8
""".strip()
        )
        == 444356092776315
    )
