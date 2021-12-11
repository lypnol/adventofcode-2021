from tool.runners.python import SubmissionPy

from collections import defaultdict


class JulesdtSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        lines = s.splitlines()
        data = defaultdict(lambda: defaultdict(int))
        for i in range(10):
            for j in range(10):
                data[i][j] = int(lines[i][j])
        flashes = 0
        for step in range(100):
            # step 1
            for i in range(10):
                for j in range(10):
                    data[i][j] += 1
            changes = True
            flashed = []
            # step 2
            while changes:
                changes = False
                for i in range(10):
                    for j in range(10):
                        if data[i][j] > 9 and (i, j) not in flashed:
                            flashes += 1
                            flashed.append((i, j))
                            changes = True
                            for x in range(-1, 2):
                                for y in range(-1, 2):
                                    if (x, y) == (0,0):
                                        continue
                                    data[i+x][j+y] += 1
            for x,y in flashed:
                data[x][y] = 0
        return flashes


def test_julesdt():
    """
    Run `python -m pytest ./day-11/part-1/julesdt.py` to test the submission.
    """
    assert (
        JulesdtSubmission().run(
            """
""".strip()
        )
        == None
    )
