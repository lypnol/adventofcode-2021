from typing import Iterable, List
from tool.runners.python import SubmissionPy


def parse(s: str) -> List[List[int]]:
    res = []
    for line in s.splitlines():
        if stripped_line := line.strip():
            res.append([int(d) for d in stripped_line])
    return res


def neighbors(table: List[List[int]], row: int, col: int) -> Iterable[int]:
    if row > 0:
        yield table[row - 1][col]
    if row + 1 < len(table):
        yield table[row + 1][col]
    if col > 0:
        yield table[row][col - 1]
    if col + 1 < len(table[0]):
        yield table[row][col + 1]



class SkaschSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        depths = parse(s)
        res = 0
        for r, row in enumerate(depths):
            for c, depth in enumerate(row):
                if all(depth < neighbor for neighbor in neighbors(depths, r, c)):
                    res += depth + 1
        return res


def test_skasch():
    """
    Run `python -m pytest ./day-09/part-1/skasch.py` to test the submission.
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
        == 15
    )
