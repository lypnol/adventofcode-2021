from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    basins_by_point = {}

    def explore(self, grid, x, y):
        if (x, y) in self.basins_by_point:
            return self.basins_by_point[(x, y)]

        if grid[y][x] == '9':
            return set()

        basin = {(x, y)}

        for dx, dy in [(1, 0), (0, 1)]:
            if y + dy < len(grid) and x + dx < len(grid[y + dy]):
                subbasin = self.explore(grid, x + dx, y + dy)
                basin.update(subbasin)

        for point in basin:
            self.basins_by_point[point] = basin

        return basin

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        self.basins_by_point = {}
        grid = [[i for i in line] for line in s.splitlines()]
        for y in range(len(grid) - 1, -1, -1):
            for x in range(len(grid[y]) - 1, -1, -1):
                self.explore(grid, x, y)

        biggest_basins = []
        score = 1
        for basin in sorted(self.basins_by_point.values(),
                            key=len,
                            reverse=True):
            if not any(
                    biggest_basin.intersection(basin)
                    for biggest_basin in biggest_basins):
                biggest_basins.append(basin)
                score *= len(basin)
                if len(biggest_basins) >= 3:
                    break

        return score


def test_th_ch():
    """
    Run `python -m pytest ./day-09/part-2/th-ch.py` to test the submission.
    """
    assert (ThChSubmission().run("""
2199943210
3987894921
9856789892
8767896789
9899965678
""".strip()) == 1134)
