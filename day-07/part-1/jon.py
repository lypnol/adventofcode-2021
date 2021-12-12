from tool.runners.python import SubmissionPy
from statistics import median


class JonSubmission(SubmissionPy):
    def run(self, s):
        l = [int(x) for x in s.strip().split(",")]

        med = int(median(l))
        return sum(abs(x - med) for x in l)


def test_jon():
    """
    Run `python -m pytest ./day-07/part-1/jon.py` to test the submission.
    """
    assert (
        JonSubmission().run(
            """
16,1,2,0,4,2,7,1,2,14
""".strip()
        )
        == 37
    )
