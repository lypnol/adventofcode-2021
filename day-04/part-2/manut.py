from tool.runners.python import SubmissionPy


class ManutSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        pass


def test_manut():
    """
    Run `python -m pytest ./day-04/part-2/manut.py` to test the submission.
    """
    assert (
        ManutSubmission().run(
            """
""".strip()
        )
        == None
    )
