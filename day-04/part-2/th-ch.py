from importlib import import_module

from tool.runners.python import SubmissionPy

Grid = import_module("day-04.part-1.th-ch").Grid


class ThChSubmission(SubmissionPy):
    def run_naive(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        lines = s.splitlines()
        nbs = lines[0].split(",")
        grids = []
        for j in range(2, len(lines), 6):
            # add lines
            rows = [[nb for nb in lines[j + k].split(" ") if nb != '']
                    for k in range(5)]
            columns = [[rows[y][x] for y in range(5)] for x in range(5)]
            grids.append(rows + columns)

        last_winner = None
        last_nb = None
        for nb in nbs:
            new_grids = [[[i for i in combination if i != nb]
                          for combination in grid] for grid in grids]
            grids = []
            for grid in new_grids:
                if any(not combination for combination in grid):
                    last_winner = grid
                    last_nb = nb
                else:
                    grids.append(grid)

        score = sum(
            [int(i) for combination in last_winner
             for i in combination]) // 2  # / 2 because lines and columns
        return int(last_nb) * score

    def run(self, s):
        lines = s.splitlines()
        nbs = lines[0].split(",")
        grids = []
        for j in range(2, len(lines), 6):
            grid = Grid()
            for y in range(5):
                x = 0
                for nb in lines[j + y].split(" "):
                    if nb != '':
                        grid.init(nb, x, y)
                        x += 1
            grids.append(grid)

        last_winner = None
        last_nb = None
        for nb in nbs:
            new_grids = []
            for grid in grids:
                if grid.mark(nb):
                    last_nb = nb
                    last_winner = grid
                else:
                    new_grids.append(grid)
            grids = new_grids

        return int(last_nb) * last_winner.get_score()


def test_th_ch():
    """
    Run `python -m pytest ./day-04/part-1/th-ch.py` to test the submission.
    """
    assert (ThChSubmission().run("""
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
""".strip()) == 1924)
