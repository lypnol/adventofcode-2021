from tool.runners.python import SubmissionPy


class BingoBoard:
    def __init__(self, board_str, board_size):
        self.board = {}
        for i, board_line in enumerate(board_str.splitlines()):
            for j, bingo_num in enumerate([int(board_line[i:i + 3]) for i in range(0, len(board_line), 3)]):
                self.board[bingo_num] = (i, j)
        self.marked_numbers = set()
        self.row_counter = [0 for _ in range(board_size)]
        self.col_counter = [0 for _ in range(board_size)]
        self.board_size = board_size

    def check_number(self, num):
        if num in self.board:
            row, col = self.board[num]
            self.marked_numbers.add(num)
            self.row_counter[row] += 1
            self.col_counter[col] += 1

    def check_win(self):
        if self.board_size in self.row_counter or self.board_size in self.col_counter:
            return True, sum([num for num in self.board if num not in self.marked_numbers])
        return False, 0


class YouyounSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        size = 5
        parsed_input = s.split("\n\n")
        draws = parsed_input[0]
        boards = set()
        for board_str in parsed_input[1:]:
            boards.add(BingoBoard(board_str, size))

        for draw in map(int, draws.split(',')):
            if len(boards) > 1:
                winner_boards = set()
                for b in boards:
                    b.check_number(draw)
                    didWin, _ = b.check_win()
                    if didWin:
                        winner_boards.add(b)
                boards = boards - winner_boards
            else:
                b = next(iter(boards))
                b.check_number(draw)
                didWin, winValue = b.check_win()
                if didWin:
                    return draw * winValue



def test_youyoun():
    """
    Run `python -m pytest ./day-04/part-1/youyoun.py` to test the submission.
    """
    assert (YouyounSubmission().run("".strip()) == None)
