import functools
import itertools
from typing import Iterable, List, Tuple

from tool.runners.python import SubmissionPy

EAST_CUCUMBER = ">"
SOUTH_CUCUMBER = "v"
EMPTY = "."


def parse(s: str) -> Tuple[List[str], int, int]:
    res = []
    nrows = 0
    ncols = 0
    for line in s.splitlines():
        if stripped_line := line.strip():
            nrows += 1
            res.extend(list(stripped_line))
            if ncols == 0:
                ncols = len(res)
    return res, nrows, ncols


@functools.lru_cache(None)
def indexes(direction: str, nrows: int, ncols: int) -> Iterable[List[int]]:
    res = []
    if direction == EAST_CUCUMBER:
        for row in range(nrows):
            res.append(list(range(ncols * row, ncols * (row + 1))))
    else:
        for col in range(ncols):
            res.append(list(range(col, nrows * ncols, ncols)))
    return res


def move(board: List[str], nrows: int, ncols: int, direction: str) -> bool:
    moved = False
    for row_pos in indexes(direction, nrows, ncols):
        first_right = board[row_pos[0]]
        first_left = board[row_pos[-1]]
        skip = False
        for left, right in zip(row_pos, row_pos[1:]):
            if skip:
                skip = False
                continue
            if board[left] == direction and board[right] == EMPTY:
                board[right] = direction
                board[left] = EMPTY
                moved = True
                skip = True
        if first_left == direction and first_right == EMPTY:
            board[row_pos[0]] = direction
            board[row_pos[-1]] = EMPTY
            moved = True
    return moved


def display(board: List[str], nrows: int, ncols: int) -> str:
    res = []
    for row in range(nrows):
        res.append("".join(board[ncols * row : ncols * (row + 1)]))
    return "\n".join(res)


class SkaschSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        board, nrows, ncols = parse(s)
        moves = 0
        for moves in itertools.count(1):
            move1 = move(board, nrows, ncols, EAST_CUCUMBER)
            move2 = move(board, nrows, ncols, SOUTH_CUCUMBER)
            if not move1 and not move2:
                break
        return moves


def test_skasch() -> None:
    """
    Run `python -m pytest ./day-25/part-1/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
""".strip()
        )
        == 58
    )
