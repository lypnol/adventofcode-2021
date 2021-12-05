from tool.runners.python import SubmissionPy

from collections import defaultdict


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        marked = defaultdict(int)  # { (x, y): nb of lines }
        for line in s.splitlines():
            beg, end = line.split(" -> ")
            x1, y1 = beg.split(",")
            x2, y2 = end.split(",")
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    marked[(x1, y)] += 1
            elif y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    marked[(x, y1)] += 1
            # Otherwise, not horizontal or vertical

        return sum(nb > 1 for nb in marked.values())


def test_th_ch():
    """
    Run `python -m pytest ./day-05/part-1/th-ch.py` to test the submission.
    """
    assert (ThChSubmission().run("""
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
""".strip()) == 5)
