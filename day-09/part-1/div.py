from tool.runners.python import SubmissionPy


class DivSubmission(SubmissionPy):
    OFFSETS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        grid = [[int(x) for x in line] for line in s.split("\n")]

        risk_levels = 0
        len_x, len_y = len(grid), len(grid[0])

        def neighbors(x, y):
            return {(x + dx, y + dy) for dx, dy in self.OFFSETS if 0 <= x + dx < len_x and 0 <= y + dy < len_y}

        for x0 in range(len_x):
            for y0 in range(len_y):
                if all(grid[x0][y0] < grid[x1][y1] for x1, y1 in neighbors(x0, y0)):
                    risk_levels += 1 + grid[x0][y0]

        return risk_levels


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
