from tool.runners.python import SubmissionPy
from collections import defaultdict


class JonSubmission(SubmissionPy):
    def run(self, s):
        lines = s.splitlines()

        draw = [int(x) for x in lines[0].split(",")]

        boards = []
        i = 2
        while i < len(lines):
            board = []
            while i < len(lines) and lines[i]:
                board.append([int(x) for x in lines[i].split(" ") if x])
                i += 1
            boards.append(board)
            i += 1

        n = len(boards)
        ny = len(boards[0])
        nx = len(boards[0][0])

        found_on_line = defaultdict(int)
        found_on_col = defaultdict(int)

        positions = defaultdict(list)

        for i, b in enumerate(boards):
            for y in range(ny):
                for x in range(nx):
                    positions[b[y][x]].append((i, y, x))

        drawn = set()
        for d in draw:
            drawn.add(d)
            win = None
            for i, x, y in positions[d]:
                found_on_line[(i, y)] += 1
                found_on_col[(i, x)] += 1
                if found_on_line[(i, y)] == nx:
                    win = i
                if found_on_col[(i, x)] == ny:
                    win = i
            if win:
                b = boards[win]
                score = 0
                for b_line in b:
                    for v in b_line:
                        if v not in drawn:
                            score += v
                return score * d

        raise Exception("No win")


def test_jon():
    """
    Run `python -m pytest ./day-04/part-1/jon.py` to test the submission.
    """
    assert (
        JonSubmission().run(
            """
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
""".strip()
        )
        == 4512
    )
