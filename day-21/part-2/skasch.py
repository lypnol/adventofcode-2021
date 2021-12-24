import collections
import functools
import re
from typing import DefaultDict, List, Set, Tuple
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
        states: DefaultDict[Tuple[int, int, int, int, int], int] = collections.defaultdict(int)
        won = [0, 0]
        states[pos1 - 1, pos2 - 1, 0, 0, 0] = 1
        valid_states: DefaultDict[Tuple[int, int], Set[Tuple[int, int, int]]] = collections.defaultdict(set)
        valid_states[0, 0].add((pos1 - 1, pos2 - 1, 0))
        for total_score in range(2 * MAX_SCORE - 1):
            for score1 in range(max(0, total_score - MAX_SCORE + 1), min(MAX_SCORE, total_score + 1)):
                score2 = total_score - score1
                for pos1_min1, pos2_min1, player in valid_states[score1, score2]:
                    count = states.pop((pos1_min1, pos2_min1, score1, score2, player))
                    for throw, n_throws in DIRAC_DICE:
                        if player == 0:
                            new_pos1 = move(pos1_min1, throw)
                            new_score1 = score1 + new_pos1
                            if new_score1 >= MAX_SCORE:
                                won[player] += n_throws * count
                            else:
                                states[new_pos1 - 1, pos2_min1, new_score1, score2, 1 - player] += n_throws * count
                                valid_states[new_score1, score2].add((new_pos1 - 1, pos2_min1, 1 - player))
                        else:
                            new_pos2 = move(pos2_min1, throw)
                            new_score2 = score2 + new_pos2
                            if new_score2 >= MAX_SCORE:
                                won[player] += n_throws * count
                            else:
                                states[pos1_min1, new_pos2 - 1, score1, new_score2, 1 - player] += n_throws * count
                                valid_states[score1, new_score2].add((pos1_min1, new_pos2 - 1, 1 - player))
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
