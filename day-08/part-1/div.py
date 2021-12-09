from tool.runners.python import SubmissionPy

from collections import defaultdict

class DivSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        count = defaultdict(int)
        for line in s.split("\n"):
            left, right = line.split(" | ")
            for digit in right.split(" "):
                if len(digit) == 2:
                    count[1] += 1
                elif len(digit) == 3:
                    count[7] += 1
                elif len(digit) == 4:
                    count[4] += 1
                elif len(digit) == 7:
                    count[8] += 1
        return sum(count.values())


def test_div():
    """
    Run `python -m pytest ./day-08/part-1/div.py` to test the submission.
    """
    assert (
        DivSubmission().run(
            """
""".strip()
        )
        == None
    )
