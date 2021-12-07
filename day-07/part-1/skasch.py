from typing import Iterable

from tool.runners.python import SubmissionPy


def parse(s: str) -> Iterable[int]:
    for number in s.split(","):
        yield int(number)


class SkaschSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        positions = sorted(parse(s))
        median = positions[len(positions) // 2]
        return sum(abs(pos - median) for pos in positions)


def test_skasch():
    """
    Run `python -m pytest ./day-07/part-1/skasch.py` to test the submission.
    """
    assert SkaschSubmission().run("""16,1,2,0,4,2,7,1,2,14""".strip()) == 37
