from tool.runners.python import SubmissionPy

from collections import defaultdict

class DivSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        overlapping_points = defaultdict(int)
        for line in s.split("\n"):
            points = line.split(" -> ")
            p1, p2 = sorted([tuple(map(int, point.split(","))) for point in points])
            x1, y1 = p1
            x2, y2 = p2

            # points are sorted,
            # so (x1, y1) <= (x2, y2)

            if y1 == y2:
                for x in range(x1, x2+1):
                    overlapping_points[(x,y1)] += 1
            elif x1 == x2:
                for y in range(y1, y2+1):
                    overlapping_points[(x1,y)] += 1

        return sum(1 for x in overlapping_points.values() if x > 1)

def test_div():
    """
    Run `python -m pytest ./day-05/part-1/div.py` to test the submission.
    """
    assert (
        DivSubmission().run(
            """
""".strip()
        )
        == None
    )
