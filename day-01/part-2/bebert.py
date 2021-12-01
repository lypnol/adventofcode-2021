from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):
    def run(self, s):
        times = 0
        a = 100000
        b = 100000
        c = 100000
        for line in s.splitlines():
            m = int(line)
            if b + c + m > a + b + c:
                times += 1
            a = b
            b = c
            c = m
        return times


def test_bebert():
    """
    Run `python -m pytest ./day-01/part-2/bebert.py` to test the submission.
    """
    assert BebertSubmission().run("""
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
""".strip()) == 5
