from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):
    def run(self, s):
        lines = [line.strip() for line in s.splitlines()]
        marked = [int(x) for x in lines[0].split(',')]
        boards = []
        checks = []
        nb_boards = 0
        for line in lines[1:]:
            if not line:
                boards.append([])
                checks.append([])
                nb_boards += 1
                continue
            boards[nb_boards - 1].append([int(x) for x in line.split(' ') if x])
            checks[nb_boards - 1].append([False for x in line.split(' ') if x])

        nb_marks = 0
        for mark in marked:
            for bid in range(nb_boards):
                for rid in range(5):
                    for cid in range(5):
                        if boards[bid][rid][cid] == mark:
                            checks[bid][rid][cid] = True
            nb_marks += 1
            if nb_marks < 5:
                continue
            for bid in range(nb_boards):
                board_won = -1
                for rid in range(5):
                    for check in checks[bid][rid]:
                        if not check:
                            break
                    else:
                        board_won = bid
                        break
                else:
                    for cid in range(5):
                        for rid in range(5):
                            if not checks[bid][rid][cid]:
                                break
                        else:
                            board_won = bid
                            break
                if board_won > -1:
                    unchecked = 0
                    for rid in range(5):
                        for cid in range(5):
                            if not checks[bid][rid][cid]:
                                unchecked += boards[bid][rid][cid]
                    return unchecked * mark
