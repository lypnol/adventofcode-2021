from collections import defaultdict

from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        n_lines_per_point = defaultdict(int)

        for line in s.splitlines():
            (p1, p2) = parse_points(line)

            if p1[0] == p2[0]:
                x = p1[0]
                sign = 1 if p2[1] > p1[1] else -1
                for y in range(p1[1], p2[1] + sign, sign):
                    p = (x, y)
                    n_lines_per_point[p] += 1
            elif p1[1] == p2[1]:
                y = p1[1]
                sign = 1 if p2[0] > p1[0] else -1
                for x in range(p1[0], p2[0] + sign, sign):
                    p = (x, y)
                    n_lines_per_point[p] += 1

        return sum(1 for n in n_lines_per_point.values() if n > 1)

def parse_points(line):
    p1, _, p2 = line.split()
    (x1, y1) = p1.split(",")
    (x2, y2) = p2.split(",")
    return ((int(x1), int(y1)), (int(x2), int(y2)))

def test_thomren():
    """
    Run `python -m pytest ./day-05/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
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
        == 5
    )
