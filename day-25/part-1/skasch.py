from typing import Iterable, List, Optional, Tuple

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


def indexes(direction: str, nrows: int, ncols: int) -> Iterable[List[int]]:
    if direction == EAST_CUCUMBER:
        for row in range(nrows):
            yield list(range(ncols * row, ncols * (row + 1)))
    else:
        for col in range(ncols):
            yield list(range(col, nrows * ncols, ncols))


def move(board: List[str], nrows: int, ncols: int, direction: str) -> None:
    for row_pos in indexes(direction, nrows, ncols):
        first_state = board[row_pos[0]]
        state = board[row_pos[0]]
        for idx, pos in enumerate(row_pos[1:]):
            if state == direction and board[pos] == EMPTY:
                state = board[pos]
                board[pos] = direction
                board[row_pos[idx]] = EMPTY
            else:
                state = board[pos]
        if state == direction and first_state == EMPTY:
            board[row_pos[0]] = direction
            board[row_pos[-1]] = EMPTY


def display(board: List[str], nrows: int, ncols: int) -> str:
    res = []
    for row in range(nrows):
        res.append("".join(board[ncols * row : ncols * (row + 1)]))
    return "\n".join(res)


class SkaschSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        board, nrows, ncols = parse(s)
        prev_board: Optional[str] = None
        moves = 0
        while (board_str := "".join(board)) != prev_board:
            moves += 1
            prev_board = board_str
            move(board, nrows, ncols, EAST_CUCUMBER)
            move(board, nrows, ncols, SOUTH_CUCUMBER)
        return moves


def test_skasch():
    """
    Run `python -m pytest ./day-25/part-1/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """v...>>.vv>
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
