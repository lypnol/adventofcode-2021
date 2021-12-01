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

    def solve(self, depths: Iterable[int]) -> int:
        prvs, nxts = itertools.tee(depths)
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
    Run `python -m pytest ./day-01/part-2/skasch.py` to test the submission.
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
        == 7
    )
