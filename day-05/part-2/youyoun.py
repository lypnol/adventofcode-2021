from collections import defaultdict

from tool.runners.python import SubmissionPy


def parse_line(l):
    x1y1, x2y2 = l.split(' -> ')
    x1, y1 = list(map(int, x1y1.split(',')))
    x2, y2 = list(map(int, x2y2.split(',')))
    return x1, y1, x2, y2


class YouyounSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        parsed_s = s.splitlines()
        intersection_points = defaultdict(int)
        for line1 in parsed_s:
            x1, y1, x2, y2 = parse_line(line1)
            if x1 == x2:
                start, end = (y1, y2) if y1 < y2 else (y2, y1)
                for e in range(start, end + 1):
                    intersection_points[(x1, e)] += 1
            elif y1 == y2:
                start, end = (x1, x2) if x1 < x2 else (x2, x1)
                for e in range(start, end + 1):
                    intersection_points[(e, y1)] += 1
            else:
                x_dir = 1 if x1 < x2 else -1
                y_dir = 1 if y1 < y2 else -1
                for i in range(0, abs(x2-x1)+1):
                    intersection_points[(x1 + x_dir * i, y1 + y_dir * i)] += 1
        return sum([intersection_points[p] > 1 for p in intersection_points])


def test_youyoun():
    """
    Run `python -m pytest ./day-05/part-1/youyoun.py` to test the submission.
    """
    assert (
            YouyounSubmission().run(
                """
    """.strip()
            )
            == None
    )
