from tool.runners.python import SubmissionPy
from math import floor


def fuel_cost(xi, x):
    # print(x, xi, (abs(xi - x) * (abs(xi - x) + 1)) / 2)
    return (abs(xi - x) * (abs(xi - x) + 1)) / 2


class YouyounSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        parsed_s = list(map(int, s.split(',')))
        mid = floor(sum(parsed_s) / len(parsed_s))
        return int(sum(fuel_cost(mid, x) for x in parsed_s))


def test_youyoun():
    """
    Run `python -m pytest ./day-07/part-2/youyoun.py` to test the submission.
    """
    assert (YouyounSubmission().run("""16,1,2,0,4,2,7,1,2,14""".strip()) == 168)
