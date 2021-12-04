from tool.runners.python import SubmissionPy


def list_sum(lst):
    res = 0
    for i in lst:
        res += int(i)
    return res

def compute_winner(board, tirage, last):
    res = 0
    print(board, tirage, last)
    for line in board:
        for elt in line:
            if not(elt in tirage):
                res += int(elt)
    return res*int(last)



def find(x, board):
    for i in range(5):
        for j in range(5):
            if (x == board[i][j]):
                return (i,j)
    return (-1,-1)

class ManutSubmission(SubmissionPy):
    def run(self, s):
        n = 5
        # m = 3
        m = 100
        f = s
        f = f.split('\n')
        tirages = f[0].split(',')
        boards = []
        coords = dict()
        winning_board = set()
        for i in range(m):
            board = []
            for j in range(n):
                coords["board_" + str(i) + "c"+str(j)] = 0
                coords["board_" + str(i) + "l" + str(j)] = 0
                board.append(list(filter(lambda x : x != '', f[2+i*(n+1) +j].split(' '))))
            coords["board_" + str(i) + "d1"] = 0
            coords["board_" + str(i) + "d2"] = 0
            boards.append(board)

        sudden_death = False
        for k in range(len(tirages)):
            ti = tirages[k]
            for i in range(len(boards)):
                if not(i in winning_board):
                    x,y = find(ti, boards[i])
                    if x != -1:
                        if x == y:
                            coords["board_" + str(i) + "d1"] += 1
                            if coords["board_" + str(i) + "d1"] == 5:
                                winning_board.add(i)
                                if sudden_death:
                                    return compute_winner(boards[i], (tirages[:k+1]), ti)
                        elif (x == 4-y):
                            coords["board_" + str(i) + "d2"] += 1
                            if coords["board_" + str(i) + "d2"] == 5:
                                winning_board.add(i)
                                if sudden_death:
                                    return compute_winner(boards[i], (tirages[:k+1]), ti)
                        coords["board_" + str(i) + "c"+str(y)] += 1
                        if coords["board_" + str(i) + "c"+str(y)] == 5:
                            winning_board.add(i)
                            if sudden_death:
                                return compute_winner(boards[i], (tirages[:k+1]), ti)
                        coords["board_" + str(i) + "l"+str(x)] += 1
                        if coords["board_" + str(i) + "l"+str(x)] == 5:
                            winning_board.add(i)
                            if sudden_death:
                                return compute_winner(boards[i], (tirages[:k+1]), ti)
                if (len(winning_board) == m-1):
                    sudden_death = True


def test_manut():
    pass
