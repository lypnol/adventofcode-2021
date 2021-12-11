import itertools
from typing import Iterable, List, Set, Tuple

from tool.runners.python import SubmissionPy

CYCLES = 100


def parse(s: str) -> List[List[int]]:
    res = []
    for line in s.splitlines():
        if stripped_line := line.strip():
            res.append([int(d) for d in stripped_line])
    return res


def neighbors(r: int, c: int, nrows: int, ncols: int) -> Iterable[Tuple[int, int]]:
    left_space = c > 0
    right_space = c + 1 < ncols
    if r > 0:
        if left_space:
            yield r - 1, c - 1
        yield r - 1, c
        if right_space:
            yield r - 1, c + 1
    if left_space:
        yield r, c - 1
    if right_space:
        yield r, c + 1
    if r + 1 < nrows:
        if left_space:
            yield r + 1, c - 1
        yield r + 1, c
        if right_space:
            yield r + 1, c + 1


def flash(board: List[List[int]], r: int, c: int) -> Set[Tuple[int, int]]:
    res = set()
    if board[r][c] < 9:
        return res
    for nr, nc in neighbors(r, c, len(board), len(board[0])):
        if board[nr][nc] > 9:
            continue
        board[nr][nc] += 1
        if board[nr][nc] > 9:
            res.add((nr, nc))
    return res


def reset(board: List[List[int]]) -> Tuple[int, int]:
    res = 0
    delta = 10
    for r, row in enumerate(board):
        for c, v in enumerate(row):
            if v > 9:
                board[r][c] = 0
                res += 1
            else:
                delta = min(delta, 10 - v)
    return res, delta


class SkaschSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        board = parse(s)
        nrows = len(board)
        ncols = len(board[0])
        res = 0
        rem = CYCLES
        delta = min(min(10 - v for v in row) for row in board)
        while rem > 0:
            steps = min(rem, delta)
            flashes = []
            for r, c in itertools.product(range(nrows), range(ncols)):
                board[r][c] += steps
                if board[r][c] > 9:
                    flashes.append((r, c))
            while flashes:
                flashes.extend(flash(board, *flashes.pop()))
            d_res, delta = reset(board)
            res += d_res
            rem -= steps
        return res


def test_skasch():
    """
    Run `python -m pytest ./day-11/part-1/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""".strip()
        )
        == 1656
    )
