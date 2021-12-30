from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        sea_cucumbers_east = set()
        sea_cucumbers_south = set()

        for j, line in enumerate(s.splitlines()):
            width = len(line)
            height = j + 1
            for i, char in enumerate(line):
                if char == ">":
                    sea_cucumbers_east.add((i, j))
                elif char == "v":
                    sea_cucumbers_south.add((i, j))

        step = 1
        while True:
            # Execute one step
            has_moved = False
            updated_sea_cucumbers_east = set()
            for i, j in sea_cucumbers_east:
                next_i, next_j = (i + 1) % width, j
                if (next_i, next_j) in sea_cucumbers_east or (
                        next_i, next_j) in sea_cucumbers_south:
                    updated_sea_cucumbers_east.add((i, j))
                else:
                    updated_sea_cucumbers_east.add((next_i, next_j))
                    has_moved = True
            sea_cucumbers_east = updated_sea_cucumbers_east

            updated_sea_cucumbers_south = set()
            for i, j in sea_cucumbers_south:
                next_i, next_j = i, (j + 1) % height
                if (next_i, next_j) in sea_cucumbers_east or (
                        next_i, next_j) in sea_cucumbers_south:
                    updated_sea_cucumbers_south.add((i, j))
                else:
                    updated_sea_cucumbers_south.add((next_i, next_j))
                    has_moved = True
            sea_cucumbers_south = updated_sea_cucumbers_south

            if not has_moved:
                break
            else:
                step += 1

        return step


def test_th_ch():
    """
    Run `python -m pytest ./day-25/part-1/th-ch.py` to test the submission.
    """
    assert (ThChSubmission().run("""
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
""".strip()) == 58)
