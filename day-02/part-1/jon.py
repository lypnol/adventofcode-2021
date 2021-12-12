from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):
    def run(self, s):
        x, d = 0, 0

        for l in s.splitlines():
            if l[0] == "f":
                x += int(l[8:])
            elif l[0] == "d":
                d += int(l[5:])
            else: # u
                d -= int(l[3:])

        return x*d


    def run_alt(self, s):
        x, d = 0, 0

        n = len(s)
        i = 0

        while i < n:
            if s[i] == "f":
                x += int(s[i+8])
                i += 10
            elif s[i] == "d":
                d += int(s[i+5])
                i += 7
            else: # u
                d -= int(s[i+3])
                i += 5

        return x*d


def test_jon():
    """
    Run `python -m pytest ./day-02/part-1/jon.py` to test the submission.
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
        == 150
    )
