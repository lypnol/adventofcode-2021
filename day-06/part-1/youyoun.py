from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        n_days = 80
        fish = [0 for _ in range(10)]
        for e in map(int, s.split(',')):
            fish[int(e) + 1] += 1
        for _ in range(n_days):
            fish[:-1] = fish[1:]
            fish[-1] = fish[0]
            fish[7] += fish[0]
            fish[0] = 0
        return sum(fish)


def test_youyoun():
    """
    Run `python -m pytest ./day-06/part-1/youyoun.py` to test the submission.
    """
    assert (
            YouyounSubmission().run(
                """
    """.strip()
            )
            == None
    )
