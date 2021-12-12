from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):
    def run(self, s):
        l = [0]*9
        for x in s.strip().split(","):
            l[int(x)] += 1

        shift = 0
        for _ in range(80):
            l[shift-2] += l[shift]
            shift = (shift+1) % 9

        return sum(l)



def test_jon():
    """
    Run `python -m pytest ./day-06/part-1/jon.py` to test the submission.
    """
    assert (
        JonSubmission().run(
            """
3,4,3,1,2
""".strip()
        )
        == 5934
    )
