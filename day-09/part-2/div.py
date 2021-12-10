from tool.runners.python import SubmissionPy

from collections import deque


class DivSubmission(SubmissionPy):
    OFFSETS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        grid = [[int(x) for x in line] for line in s.split("\n")]

        low_points = dict()
        low_points_seq = 0
        len_x, len_y = len(grid), len(grid[0])

        def neighbors(x, y):
            return {(x + dx, y + dy) for dx, dy in self.OFFSETS if 0 <= x + dx < len_x and 0 <= y + dy < len_y}

        for x0 in range(len_x):
            for y0 in range(len_y):
                if all(grid[x0][y0] < grid[x1][y1] for x1, y1 in neighbors(x0, y0)):
                    low_points[(x0, y0)] = low_points_seq
                    low_points_seq += 1

        basins_grid = [[None for _ in range(len_y)] for _ in range(len_x)]
        # at (x,y) we store the basin ID (which is the index of the low_point)

        for i in range(10):
            copy_basins_grid = [[x for x in line] for line in basins_grid]
            for x in range(len_x):
                for y in range(len_y):
                    if (x, y) in low_points:
                        copy_basins_grid[x][y] = low_points[(x, y)]
                        continue

                    if grid[x][y] == 9:
                        continue

                    adjacent_basins = set()
                    for x1, y1 in neighbors(x, y):
                        if basins_grid[x1][y1] is not None:
                            adjacent_basins.add(basins_grid[x1][y1])

                    if len(adjacent_basins) == 1:
                        copy_basins_grid[x][y] = adjacent_basins.pop()
            basins_grid = copy_basins_grid

        basins_sizes = [0] * len(low_points)
        for x in range(len_x):
            for y in range(len_y):
                if basins_grid[x][y] is not None:
                    basins_sizes[basins_grid[x][y]] += 1
        basins_sizes.sort(reverse=True)
        s1, s2, s3 = basins_sizes[:3]
        return s1 * s2 * s3


def test_div():
    """
    Run `python -m pytest ./day-09/part-1/div.py` to test the submission.
    """
    assert (
        DivSubmission().run(
            """
""".strip()
        )
        == None
    )
