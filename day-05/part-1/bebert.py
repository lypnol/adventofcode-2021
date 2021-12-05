from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):
    def run(self, s):
        world = [[0 for __ in range(1000)] for _ in range(1000)]
        for line in s.splitlines():
            xy1s, xy2s = line.split(' -> ')
            x1, y1 = [int(k) for k in xy1s.split(',')]
            x2, y2 = [int(k) for k in xy2s.split(',')]
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    world[y][x1] += 1
            elif y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    world[y1][x] += 1
        total = 0
        for row in world:
            for k in row:
                if k >= 2:
                    total += 1
        return total


def test_bebert():
    """
    Run `python -m pytest ./day-05/part-1/bebert.py` to test the submission.
    """
    assert BebertSubmission().run("""
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
""".strip()) == 5
