from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        pass


def test_thomren():
    """
    Run `python -m pytest ./day-23/part-2/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
""".strip()
        )
        == None
    )
