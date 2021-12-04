from typing import Dict, Iterable, List, Tuple
from tool.runners.python import SubmissionPy


class Board:

    SIZE = 5

    numbers: List[List[str]]
    rev_map: Dict[str, Tuple[int, int]]
    marked: List[List[bool]]
    unmarked: int

    def __init__(self, input: Iterable[str]):
        self.numbers = []
        self.rev_map = {}
        self.unmarked = 0
        for row, line in zip(range(self.SIZE), input):
            self.numbers.append([])
            for col, value in enumerate(line.split()):
                self.numbers[-1].append(value)
                self.rev_map[value] = (row, col)
                self.unmarked += int(value)
        self.marked = [[False] * self.SIZE for _ in range(self.SIZE)]

    def bingo(self, row: int, col: int) -> bool:
        if all(self.marked[row]):
            return True
        if all(marked_row[col] for marked_row in self.marked):
            return True
        return False

    def mark(self, number: str) -> bool:
        if number in self.rev_map:
            row, col = self.rev_map[number]
            self.marked[row][col] = True
            self.unmarked -= int(number)
            return self.bingo(row, col)
        return False

    def score(self, number: str) -> int:
        return self.unmarked * int(number)


class SkaschSubmission(SubmissionPy):
    def parse(self, s: str) -> Tuple[List[str], List[Board]]:
        iter_s = iter(s.splitlines())
        numbers = next(iter_s).split(",")
        boards = []
        next(iter_s)
        try:
            while True:
                boards.append(Board(iter_s))
                next(iter_s)
        except StopIteration:
            pass
        return numbers, boards

    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        numbers, boards = self.parse(s)
        ongoing_boards = set(range(len(boards)))
        for number in numbers:
            to_remove = set()
            for idx in ongoing_boards:
                if boards[idx].mark(number):
                    to_remove.add(idx)
                    if len(ongoing_boards) == len(to_remove):
                        return boards[idx].score(number)
            ongoing_boards -= to_remove
        raise ValueError("Invalid input: no winner")


def test_skasch():
    """
    Run `python -m pytest ./day-04/part-1/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
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
        == 1924
    )
