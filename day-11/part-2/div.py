from tool.runners.python import SubmissionPy

from collections import deque


class DivSubmission(SubmissionPy):
    OFFSETS = [(0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1), (1, 1), (1, 0), (1, -1)]

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        grid = [[int(x) for x in line] for line in s.split("\n")]
        len_x, len_y = len(grid), len(grid[0])

        def neighbors(x, y):
            return ((x + dx, y + dy) for dx, dy in self.OFFSETS if 0 <= x + dx < len_x and 0 <= y + dy < len_y)

        step = 0
        while True:
            for x in range(len_x):
                for y in range(len_y):
                    grid[x][y] += 1

            flashes = set()
            to_visit = deque()
            for x in range(len_x):
                for y in range(len_y):
                    if grid[x][y] > 9:
                        flashes.add((x, y))
                        to_visit.append((x, y))

            while to_visit:
                x0, y0 = to_visit.pop()
                for x1, y1 in neighbors(x0, y0):
                    grid[x1][y1] += 1
                    if grid[x1][y1] > 9 and not (x1, y1) in flashes:
                        flashes.add((x1, y1))
                        to_visit.append((x1, y1))

            for x, y in flashes:
                grid[x][y] = 0
            step += 1

            if len(flashes) == len_x * len_y:
                return step


def test_div():
    """
    Run `python -m pytest ./day-11/part-1/div.py` to test the submission.
    """
    assert (
        DivSubmission().run(
            """
""".strip()
        )
        == None
    )
