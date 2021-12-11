from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        parsed_s = list(map(int, s.split(',')))
        mid = sorted(parsed_s)[len(parsed_s) // 2]
        return sum([abs(x - mid) for x in parsed_s])


def test_youyoun():
    """
    Run `python -m pytest ./day-07/part-1/youyoun.py` to test the submission.
    """
    assert (
        YouyounSubmission().run(
            """
""".strip()
        )
        == None
    )
