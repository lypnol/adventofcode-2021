from itertools import product

from tool.runners.python import SubmissionPy

N_STEPS = 100


class ThomrenSubmission(SubmissionPy):
    def run(self, s, n_steps=N_STEPS):
        """
        :param s: input in string format
        :return: solution flag
        """
        octopuses = [[int(c) for c in lines] for lines in s.splitlines()]
        height, width = len(octopuses), len(octopuses[0])
        n_flashes = 0

        for _ in range(n_steps):
            flash_stack = []
            for i, j in product(range(height), range(width)):
                octopuses[i][j] += 1
                if octopuses[i][j] == 10:
                    flash_stack.append((i, j))

            while len(flash_stack):
                (i, j) = flash_stack.pop()
                octopuses[i][j] = 0
                n_flashes += 1
                for x, y in neighbors(i, j, height, width):
                    # octopuses with 0 have already flashed during this step
                    octopuses[x][y] += int(octopuses[x][y] > 0)
                    if octopuses[x][y] == 10:
                        flash_stack.append((x, y))

        return n_flashes


def neighbors(i, j, height, width):
    for di, dj in [
        (-1, 0),
        (0, -1),
        (-1, -1),
        (1, 0),
        (0, 1),
        (1, 1),
        (1, -1),
        (-1, 1),
    ]:
        (x, y) = (i + di, j + dj)
        if x >= 0 and y >= 0 and x < height and y < width:
            yield (x, y)


def test_thomren():
    """
    Run `python -m pytest ./day-11/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""".strip()
        )
        == 1656
    )
