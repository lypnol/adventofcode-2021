import re
from typing import Iterator, List
from tool.runners.python import SubmissionPy


REGEX = re.compile(r"Player [1-2] starting position: ([0-9]+)")


def deterministic_dice() -> Iterator[int]:
    v = 6
    last = 3
    rem = 0
    while True:
        yield v
        v += 9
        last += 3
        if rem > 0:
            v -= 100 * rem
            rem = 0
        if last > 100:
            last -= 100
            v -= 100 * last
            rem = 3 - last


def parse(s: str) -> List[int]:
    vs: List[int] = []
    for line in s.splitlines():
        if stripped_line := line.strip():
            m = REGEX.match(stripped_line)
            assert m is not None
            vs.append(int(m.group(1)))
    return vs


BOARD_SIZE = 10
MAX_SCORE = 1000


def move(pos: int, throw: int) -> int:
    return (pos + throw - 1) % BOARD_SIZE + 1


class SkaschSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        dice = deterministic_dice()
        pos = parse(s)
        scores = [0, 0]
        player = 0
        n_throws = 0
        while max(scores) < MAX_SCORE:
            pos[player] = move(pos[player], next(dice))
            scores[player] += pos[player]
            n_throws += 3
            player = 1 - player
        return n_throws * min(scores)


def test_skasch() -> None:
    """
    Run `python -m pytest ./day-21/part-1/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
Player 1 starting position: 4
Player 2 starting position: 8
""".strip()
        )
        == 739785
    )
