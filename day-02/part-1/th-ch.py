from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        pos = 0
        depth = 0
        for command in s.splitlines():
            direction, value = command.split(" ")
            if direction == "forward":
                pos += int(value)
            elif direction == "down":
                depth += int(value)
            elif direction == "up":
                depth -= int(value)

        return pos*depth


def test_th_ch():
    """
    Run `python -m pytest ./day-02/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
forward 5
down 5
forward 8
up 3
down 8
forward 2
""".strip()
        )
        == 150
    )
