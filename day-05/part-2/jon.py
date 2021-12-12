from tool.runners.python import SubmissionPy
from collections import defaultdict


class JonSubmission(SubmissionPy):
    def run(self, s):
        m = defaultdict(int)

        for l in s.splitlines():
            c1, _, c2 = l.split(" ")
            x1, y1 = (int(x) for x in c1.split(","))
            x2, y2 = (int(x) for x in c2.split(","))

            if x1 == x2:
                for y in rrange(y1, y2):
                    m[(x1, y)] += 1
            elif y1 == y2:
                for x in rrange(x1, x2):
                    m[(x, y1)] += 1
            else:
                n = abs(x1-x2)
                dx, dy = (1 if x2 > x1 else -1, 1 if y2 > y1 else -1)
                for i in range(n+1):
                    m[(x1+i*dx, y1+i*dy)] += 1

        return sum(1 for v in m.values() if v >= 2)


def rrange(a, b):
    return range(min(a, b), max(a, b)+1)


def test_jon():
    """
    Run `python -m pytest ./day-05/part-2/jon.py` to test the submission.
    """
    assert (
        JonSubmission().run(
            """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""".strip()
        )
        == 12
    )
