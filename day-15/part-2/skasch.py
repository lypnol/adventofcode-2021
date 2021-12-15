import heapq
from typing import Iterable, List, Tuple
from tool.runners.python import SubmissionPy


def parse(s: str) -> List[List[int]]:
    res = []
    for line in s.splitlines():
        if stripped_line := line.strip():
            res.append([int(d) for d in stripped_line])
    return res


REPEAT = 5


class SkaschSubmission(SubmissionPy):
    def neighbors(self, r: int, c: int) -> Iterable[Tuple[int, int]]:
        if r > 0:
            yield r - 1, c
        if r + 1 < self.nrows:
            yield r + 1, c
        if c > 0:
            yield r, c - 1
        if c + 1 < self.ncols:
            yield r, c + 1

    def repeat(self, board: List[List[int]]) -> List[List[int]]:
        self.nrows = len(board) * REPEAT
        self.ncols = len(board[0]) * REPEAT
        res = [[0] * self.ncols for _ in range(self.nrows)]
        for row in range(REPEAT):
            for col in range(REPEAT):
                for r, line in enumerate(board):
                    for c, v in enumerate(line):
                        res[r + row * len(board)][c + col * len(board[0])] = (v + row + col - 1) % 9 + 1
        return res

    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        board = self.repeat(parse(s))
        start_risk = 0
        end_risk = board[-1][-1]
        minrisk_start = [[float("inf")] * self.ncols for _ in range(self.nrows)]
        minrisk_start[0][0] = board[0][0]
        minrisk_end = [[float("inf")] * self.ncols for _ in range(self.nrows)]
        minrisk_end[-1][-1] = end_risk
        q = [(start_risk + end_risk, start_risk, end_risk, (0, 0), (self.nrows - 1, self.ncols - 1))]
        while q:
            risk, risk1, risk2, pos1, pos2 = heapq.heappop(q)
            if sum(abs(p1 - p2) for p1, p2 in zip(pos1, pos2)) == 1:
                return risk
            for nr, nc in self.neighbors(*pos1):
                nrisk1 = risk1 + board[nr][nc]
                if nrisk1 >= minrisk_start[nr][nc]:
                    continue
                minrisk_start[nr][nc] = nrisk1
                heapq.heappush(q, (nrisk1 + risk2, nrisk1, risk2, (nr, nc), pos2))
            for nr, nc in self.neighbors(*pos2):
                nrisk2 = risk2 + board[nr][nc]
                if nrisk2 >= minrisk_end[nr][nc]:
                    continue
                minrisk_end[nr][nc] = nrisk2
                heapq.heappush(q, (risk1 + nrisk2, risk1, nrisk2, pos1, (nr, nc)))
        raise ValueError


def test_skasch() -> None:
    """
    Run `python -m pytest ./day-15/part-2/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""".strip()
        )
        == 315
    )
