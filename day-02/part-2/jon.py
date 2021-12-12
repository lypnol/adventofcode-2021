from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):
    def run(self, s):
        x, d, aim = 0, 0, 0

        for l in s.splitlines():
            if l[0] == "f":
                v = int(l[8:])
                x += v
                d += aim*v 
            elif l[0] == "d":
                aim += int(l[5:])
            else: # u
                aim -= int(l[3:])

        return x*d


def test_jon():
    """
    Run `python -m pytest ./day-02/part-2/jon.py` to test the submission.
    """
    assert (
        JonSubmission().run(
            """forward 5
down 5
forward 8
up 3
down 8
forward 2
""".strip()
        )
        == 900
    )
