from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        crabs = sorted([int(crab) for crab in s.split(",")])
        median = (crabs[len(crabs) // 2 - 1] + crabs[len(crabs) // 2]) // 2
        return sum(abs(crab - median) for crab in crabs)


def test_th_ch():
    """
    Run `python -m pytest ./day-07/part-1/th-ch.py` to test the submission.
    """
    assert (ThChSubmission().run("""
16,1,2,0,4,2,7,1,2,14
""".strip()) == 37)
