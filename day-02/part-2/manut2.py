from tool.runners.python import SubmissionPy
from functools import reduce


class ManutSubmission(SubmissionPy):
    def run(self, s):
        return reduce(lambda x, y: x * y, reduce(lambda acc, arg: [acc[0] + int(arg.split()[1]), acc[1] + (int(arg.split()[1]) * acc[2]), acc[2]] if arg.split()[0] == "forward" else [acc[0], acc[1], acc[2] + int(arg.split()[1])], (s.replace("up ", "down -").split('\n')), [0, 0, 0])[:-1])


def test_manut():
    """
    Run `python -m pytest ./day-02/part-2/manut.py` to test the submission.
    """
    pass
