from tool.runners.python import SubmissionPy


class JulesdtSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        depth = 0
        horizontal = 0
        aim = 0
        for line in s.split("\n"):
            move, amount = line.split()
            # print(move, amount)
            amount = int(amount)
            if move == "forward":
                horizontal += amount
                depth += aim * amount
            elif move == "down":
                aim += amount
            elif move == "up":
                aim -= amount
        return depth * horizontal


def test_julesdt():
    """
    Run `python -m pytest ./day-02/part-1/julesdt.py` to test the submission.
    """
    assert (
        JulesdtSubmission().run(
            """
""".strip()
        )
        == None
    )
