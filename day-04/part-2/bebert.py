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
        last_winning = -1
        boards_won = [False for _ in range(nb_boards)]
        for mark in marked:
            for bid in range(nb_boards):
                if boards_won[bid]:
                    continue
                for rid in range(5):
                    for cid in range(5):
                        if boards[bid][rid][cid] == mark:
                            checks[bid][rid][cid] = True
            nb_marks += 1
            if nb_marks < 5:
                continue
            for bid in range(nb_boards):
                if boards_won[bid]:
                    continue
                for rid in range(5):
                    for check in checks[bid][rid]:
                        if not check:
                            break
                    else:
                        boards_won[bid] = True
                        break
                else:
                    for cid in range(5):
                        for rid in range(5):
                            if not checks[bid][rid][cid]:
                                break
                        else:
                            boards_won[bid] = True
                            break
            nb_winning = nb_boards
            for bid in range(nb_boards):
                if not boards_won[bid]:
                    nb_winning -= 1
                    last_winning = bid
            for won in boards_won:
                if not won:
                    break
            else:
                unchecked = 0
                for rid in range(5):
                    for cid in range(5):
                        if not checks[last_winning][rid][cid]:
                            unchecked += boards[last_winning][rid][cid]
                return unchecked * mark
