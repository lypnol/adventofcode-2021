from tool.runners.python import SubmissionPy
from statistics import median


class JonSubmission(SubmissionPy):
    def run(self, s):
        l = [int(x) for x in s.strip().split(",")]

        def fuel(pos):
            return sum(cost(abs(x - pos)) for x in l)

        return min(fuel(pos) for pos in range(min(l), max(l)+1))


def cost(n):
    return n*(n+1) // 2


def test_jon():
    """
    Run `python -m pytest ./day-07/part-2/jon.py` to test the submission.
    """
    assert (
        JonSubmission().run(
            """
16,1,2,0,4,2,7,1,2,14
""".strip()
        )
        == 168
    )
