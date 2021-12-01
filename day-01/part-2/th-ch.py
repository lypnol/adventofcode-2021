from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    SLIDING_WINDOW_SIZE = 3

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        depths = [int(depth) for depth in s.splitlines()]
        return sum(depths[i+self.SLIDING_WINDOW_SIZE] > depths[i] for i in range(len(depths) - self.SLIDING_WINDOW_SIZE))


def test_th_ch():
    """
    Run `python -m pytest ./day-01/part-2/th-ch.py` to test the submission.
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
        == 5
    )
