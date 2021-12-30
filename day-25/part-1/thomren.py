from tool.runners.python import SubmissionPy


EAST_CUCUMBER = 0
SOUTH_CUCUMBER = 1


class ThomrenSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        lines = s.splitlines()
        height, width = len(lines), len(lines[0])
        sea_floor = dict()
        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                if c == ">":
                    sea_floor[(i, j)] = EAST_CUCUMBER
                elif c == "v":
                    sea_floor[(i, j)] = SOUTH_CUCUMBER

        n_steps = 0
        moved = True
        while moved:
            sea_floor, moved = step(sea_floor, height, width)
            n_steps += 1

        return n_steps


def step(sea_floor, height, width):
    intermediate_sea_floor = dict()
    moved = False
    for (i, j), cucumber in sea_floor.items():
        if cucumber == SOUTH_CUCUMBER:
            continue
        k = (j + 1) % width
        if (i, k) not in sea_floor:
            intermediate_sea_floor[(i, k)] = EAST_CUCUMBER
            moved = True
        else:
            intermediate_sea_floor[(i, j)] = cucumber

    next_sea_floor = dict(intermediate_sea_floor)
    for (i, j), cucumber in sea_floor.items():
        if cucumber == EAST_CUCUMBER:
            continue
        p = (i + 1) % height
        if (
            not sea_floor.get((p, j)) == SOUTH_CUCUMBER
            and (p, j) not in intermediate_sea_floor
        ):
            next_sea_floor[(p, j)] = SOUTH_CUCUMBER
            moved = True
        else:
            next_sea_floor[(i, j)] = cucumber

    return next_sea_floor, moved


def test_thomren():
    """
    Run `python -m pytest ./day-25/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
""".strip()
        )
        == 58
    )
