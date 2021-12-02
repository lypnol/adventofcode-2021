from tool.runners.python import SubmissionPy
from functools import reduce


class ManutSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        return reduce(lambda x,y:x*y, reduce(lambda acc,arg: [acc[0]+int(arg.split()[1]), acc[1]] if arg.split()[0] == "down" else [acc[0], acc[1]+int(arg.split()[1])], sorted(s.replace("up ", "down -").split('\n')), [0,0]))


def test_manut():
    """
    Run `python -m pytest ./day-02/part-1/manut.py` to test the submission.
    """
    pass
