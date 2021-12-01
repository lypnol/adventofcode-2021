from tool.runners.python import SubmissionPy


class DivSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        l = [int(x) for x in s.split()]
        n = len(l)
        l3 = [l[x] + l[x-1] + l[x-2] for x in range(2, n)]
        return sum(1 for x in range(1, len(l3)) if l3[x]>l3[x-1])
        pass


def test_div():
    """
    Run `python -m pytest ./day-01/part-2/div.py` to test the submission.
    """
    assert (
        DivSubmission().run(
            """
""".strip()
        )
        == None
    )
