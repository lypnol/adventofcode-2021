from tool.runners.python import SubmissionPy


class ManutSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here

        s = s.split('\n')
        x_pos = 0
        depth = 0
        for line in s:
            coord = line.split(' ')
            if coord[0] == "forward":
                x_pos += int(coord[1])
            elif coord[0] == "down":
                depth += int(coord[1])
            elif coord[0] == "up":
                depth -= int(coord[1])
        return (x_pos * depth)


def test_manut():
    """
    Run `python -m pytest ./day-02/part-1/manut.py` to test the submission.
    """
    pass
