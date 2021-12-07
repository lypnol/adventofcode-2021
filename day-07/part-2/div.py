from tool.runners.python import SubmissionPy


class DivSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        positions = [int(x) for x in s.split(",")]
        min_pos, max_pos = min(positions), max(positions)
        return min(sum(((abs(x-x0))*(abs(x-x0)+1))>>1 for x0 in positions) for x in range(min_pos, max_pos+1))



def test_div():
    """
    Run `python -m pytest ./day-07/part-1/div.py` to test the submission.
    """
    assert (
        DivSubmission().run(
            """
""".strip()
        )
        == None
    )
