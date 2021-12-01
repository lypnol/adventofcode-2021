from tool.runners.python import SubmissionPy


class DivSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        l = [int(x) for x in s.split()]
        n = len(l)
        return sum(1 for x in range(1, n) if l[x]>l[x-1])


def test_div():
    """
    Run `python -m pytest ./day-01/part-1/div.py` to test the submission.
    """
    assert (
        DivSubmission().run(
            """
""".strip()
        )
        == None
    )
