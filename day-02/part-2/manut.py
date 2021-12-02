from tool.runners.python import SubmissionPy


class ManutSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        x_pos = 0
        depth = 0
        aim = 0
        s = s.split('\n')
        for line in s:
            coord = line.split(' ')
            if coord[0] == "forward":
                x_pos += int(coord[1])
                depth += int(coord[1])*aim
            elif coord[0] == "down":
                aim += int(coord[1])
            elif coord[0] == "up":
                aim -= int(coord[1])
        return (x_pos * depth)


def test_manut():
    """
    Run `python -m pytest ./day-02/part-2/manut.py` to test the submission.
    """
    pass
