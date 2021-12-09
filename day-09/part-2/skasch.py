from typing import Iterable, List
import itertools
import heapq
from tool.runners.python import SubmissionPy


def parse(s: str) -> List[List[int]]:
    res = []
    for line in s.splitlines():
        if stripped_line := line.strip():
            res.append([int(d) for d in stripped_line])
    return res


def neighbors(table: List[List[int]], row: int, col: int) -> Iterable[int]:
    if row > 0:
        yield row - 1, col
    if row + 1 < len(table):
        yield row + 1, col
    if col > 0:
        yield row, col - 1
    if col + 1 < len(table[0]):
        yield row, col + 1


MAX_DEPTH = 9


class SkaschSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        depths = parse(s)
        visited = set()
        basins = []
        nrows = len(depths)
        ncols = len(depths[0])
        for r, c in itertools.product(range(nrows), range(ncols)):
            if (r, c) in visited or depths[r][c] == MAX_DEPTH:
                continue
            q = [(r, c)]
            basin_size = 0
            while q:
                r, c = q.pop()
                if (r, c) in visited:
                    continue
                visited.add((r, c))
                basin_size += 1
                for nr, nc in neighbors(depths, r, c):
                    if (nr, nc) in visited or depths[nr][nc] == MAX_DEPTH:
                        continue
                    q.append((nr, nc))
            if len(basins) >= 3:
                heapq.heappushpop(basins, basin_size)
            else:
                heapq.heappush(basins, basin_size)
        return basins[0] * basins[1] * basins[2]


def test_skasch():
    """
    Run `python -m pytest ./day-09/part-2/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
2199943210
3987894921
9856789892
8767896789
9899965678
""".strip()
        )
        == 1134
    )
