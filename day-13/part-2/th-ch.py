from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        dots_coords, instructions = s.split("\n\n")
        dots = set()
        for line in dots_coords.splitlines():
            x, y = line.split(",")
            dots.add((int(x), int(y)))

        for instruction in instructions.splitlines():
            axis, nb = instruction.replace("fold along ", "").split("=")
            nb = int(nb)
            old_dots = dots
            dots = set()
            for x, y in old_dots:
                if axis == "y" and y <= nb:
                    dots.add((x, y))
                    continue
                if axis == "x" and x <= nb:
                    dots.add((x, y))
                    continue

                # need to change the dot
                if axis == "y":
                    dots.add((x, nb - (y - nb)))
                elif axis == "x":
                    dots.add((nb - (x - nb), y))

        res = []
        for y in range(max(y for _, y in dots) + 1):
            res.append("".join("#" if (x, y) in dots else "."
                               for x in range(max(x for x, _ in dots) + 2)))

        return "\n".join(res)


def test_th_ch():
    """
    Run `python -m pytest ./day-13/part-1/th-ch.py` to test the submission.
    """
    assert (ThChSubmission().run("""
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""".strip()) == """\
#####.
#...#.
#...#.
#...#.
#####.""")
