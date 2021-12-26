from tool.runners.python import SubmissionPy
import numpy as np


class Octopus:
    def __init__(self, init_level):
        self.energy_level = init_level
        self.adjacent_octopi = []
        self.adjacent_pos = set()

        self.did_flash = False

    def __repr__(self):
        return f"Energy: {self.energy_level}, Flash: {self.did_flash}"

    def add_adjecten_octopi(self, octopus, pos):
        if pos not in self.adjacent_pos:
            self.adjacent_octopi.append(octopus)
            self.adjacent_pos.add(pos)

    def increase_level(self):
        self.energy_level += 1
        self.flash()

    def flash(self):
        if not self.did_flash and self.energy_level > 9:
            self.did_flash = True
            for octopus in self.adjacent_octopi:
                octopus.increase_level()

    def new_step(self):
        if self.did_flash:
            self.energy_level = 0
        self.did_flash = False


def print_octopus_grid(octopi):
    arr = ''
    _bold_escape = '\033[1m', '\033[0m'
    n = int(np.sqrt(len(octopi)))
    for i in range(n):
        line = ''
        for j in range(n):
            level = octopi[(i, j)].energy_level
            line += f"{_bold_escape[0] if level == 0 else ''}{str(level)}{_bold_escape[1] if level == 0 else ''}"
        arr += line + '\n'
    print(arr)
    print()
    return


def adjacent_points(arr, i, j):
    neighbours = []
    if i > 0:
        neighbours.append((i - 1, j))
    if i < len(arr) - 1:
        neighbours.append((i + 1, j))
    if j > 0:
        neighbours.append((i, j - 1))
    if j < len(arr[0]) - 1:
        neighbours.append((i, j + 1))
    if i > 0 and j > 0:
        neighbours.append((i - 1, j - 1))
    if i > 0 and j < len(arr[0]) - 1:
        neighbours.append((i - 1, j + 1))
    if i < len(arr) - 1 and j > 0:
        neighbours.append((i + 1, j - 1))
    if i < len(arr) - 1 and j < len(arr[0]) - 1:
        neighbours.append((i + 1, j + 1))
    return neighbours


class YouyounSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        arr = [list(map(int, list(x))) for x in s.splitlines()]
        octopi = {}
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                octopus = Octopus(int(arr[i][j]))
                octopi[(i, j)] = octopus
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                octopus = octopi[(i, j)]
                neighbour_pos = adjacent_points(arr, i, j)
                for nei in neighbour_pos:
                    octopus.add_adjecten_octopi(octopi[nei], nei)
        i = 0
        while True:
            # print_octopus_grid(octopi)
            for octopus in octopi.values():
                octopus.increase_level()
            counter = 0
            for octopus in octopi.values():
                octopus.new_step()
                counter += octopus.energy_level
            if counter == 0:
                return i + 1
            i += 1


def test_youyoun():
    """
    Run `python -m pytest ./day-11/part-1/youyoun.py` to test the submission.
    """
    assert (
            YouyounSubmission().run(
                """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".strip()
            )
            == 195
    )
