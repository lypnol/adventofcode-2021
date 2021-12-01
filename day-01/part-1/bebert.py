from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):
    def run(self, s):
        times = 0
        n = 100000
        for line in s.splitlines():
            m = int(line)
            if m > n:
                times += 1
            n = m
        return times


def test_bebert():
    """
    Run `python -m pytest ./day-01/part-1/bebert.py` to test the submission.
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
""".strip()) == 7
