import itertools
from typing import Iterable, TypeVar
from tool.runners.python import SubmissionPy


T = TypeVar("T")


def skip(iterator: Iterable[T], n: int = 1) -> Iterable[T]:
    for _ in range(n):
        next(iterator)
    yield from iterator


class SkaschSubmission(SubmissionPy):

    def parse(self, s: str) -> Iterable[int]:
        for line in s.splitlines():
            if stripped_line := line.strip():
                yield int(stripped_line)

    def sliding_sums_3(self, depths: Iterable[int]) -> Iterable[int]:
        d1s, d2s, d3s = itertools.tee(depths, 3)
        for d1, d2, d3 in zip(d1s, skip(d2s), skip(d3s, 2)):
            yield d1 + d2 + d3

    def solve(self, depths: Iterable[int]) -> int:
        depth_sums = self.sliding_sums_3(depths)
        prvs, nxts = itertools.tee(depth_sums)
        return sum(prv < nxt for prv, nxt in zip(prvs, skip(nxts)))

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        return self.solve(self.parse(s))


def test_skasch():
    """
    Run `python -m pytest ./day-01/part-1/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
199
200
208
210
200
207
240
269
260
263
""".strip()
        )
        == 5
    )
