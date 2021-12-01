from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        depths = [int(depth) for depth in s.splitlines()]
        return sum(depths[i+1] > depths[i] for i in range(len(depths)-1))



def test_th_ch():
    """
    Run `python -m pytest ./day-01/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
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
""".strip()
        )
        == 7
    )
