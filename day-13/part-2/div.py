from tool.runners.python import SubmissionPy


class DivSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        blocks = s.split("\n\n")
        raw_points = blocks[0].split("\n")

        points = set()
        for raw_point in raw_points:
            x,y = tuple(map(int, raw_point.split(",")))
            points.add((x,y))

        instructions = blocks[1].split("\n")
        for instruction in instructions:
            axis, line_str = instruction[11:].split("=")
            line = int(line_str)

            new_points = set()
            for x,y in points:
                if axis == "x":
                    if x < line:
                        new_points.add((x,y))
                    else:
                        new_points.add((line-(x-line),y))
                elif axis == "y":
                    if y < line:
                        new_points.add((x,y))
                    else:
                        new_points.add((x,(line-(y-line))))
            points = new_points

        max_x = max((x for x,_ in points))
        max_y = max((y for _,y in points))

        lines = []
        for y in range(max_y+1):
            lines.append("".join(["#" if (x,y) in points else "." for x in range(max_x+1)]))

        return "\n".join(lines) # too lazy to identify the letters from the string :)

def test_div():
    """
    Run `python -m pytest ./day-13/part-1/div.py` to test the submission.
    """
    assert (
        DivSubmission().run(
            """
""".strip()
        )
        == None
    )
