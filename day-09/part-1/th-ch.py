from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        grid = [[int(i) for i in line] for line in s.splitlines()]
        risk_level = 0
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                is_lowest = True
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if 0 <= y + dy < len(grid) and 0 <= x + dx < len(
                            grid[y + dy]) and grid[y][x] >= grid[y + dy][x +
                                                                         dx]:
                        is_lowest = False
                        break
                if is_lowest:
                    risk_level += grid[y][x] + 1

        return risk_level


def test_th_ch():
    """
    Run `python -m pytest ./day-09/part-1/th-ch.py` to test the submission.
    """
    assert (ThChSubmission().run("""
2199943210
3987894921
9856789892
8767896789
9899965678
""".strip()) == 15)
