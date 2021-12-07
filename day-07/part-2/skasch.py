from typing import Iterable

from tool.runners.python import SubmissionPy


def parse(s: str) -> Iterable[int]:
    for number in s.split(","):
        yield int(number)


def compute(positions, mean):
    return sum((abs(pos - mean) * (abs(pos - mean) + 1)) // 2 for pos in positions)


class SkaschSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        positions = list(parse(s))
        mean = round(sum(positions) / len(positions))
        res = compute(positions, mean)
        too_high = False
        while compute(positions, mean - 1) < res:
            mean -= 1
            res = compute(positions, mean)
            too_high = True
        if not too_high:
            while compute(positions, mean + 1) < res:
                mean += 1
                res = compute(positions, mean)
        return res


def test_skasch():
    """
    Run `python -m pytest ./day-07/part-1/skasch.py` to test the submission.
    """
    assert SkaschSubmission().run("""16,1,2,0,4,2,7,1,2,14""".strip()) == 206
