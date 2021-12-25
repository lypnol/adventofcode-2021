from tool.runners.python import SubmissionPy


class SkaschSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        pass


def test_skasch():
    """
    Run `python -m pytest ./day-25/part-2/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
""".strip()
        )
        == None
    )
