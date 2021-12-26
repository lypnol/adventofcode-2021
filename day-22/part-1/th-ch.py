from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        cubes_on = set()
        for instruction in s.splitlines():
            on_or_off, coords = instruction.split(" ")
            x_coords, y_coords, z_coords = coords.split(",")
            x_min, x_max = x_coords.replace("x=", "").split("..")
            y_min, y_max = y_coords.replace("y=", "").split("..")
            z_min, z_max = z_coords.replace("z=", "").split("..")
            x_min, x_max, y_min, y_max, z_min, z_max = int(x_min), int(
                x_max), int(y_min), int(y_max), int(z_min), int(z_max)

            x_min, x_max = max(-50, x_min), min(50, x_max)
            y_min, y_max = max(-50, y_min), min(50, y_max)
            z_min, z_max = max(-50, z_min), min(50, z_max)

            for z in range(z_min, z_max + 1):
                for y in range(y_min, y_max + 1):
                    for x in range(x_min, x_max + 1):
                        if on_or_off == "on":
                            cubes_on.add((x, y, z))
                        elif (x, y, z) in cubes_on:
                            cubes_on.remove((x, y, z))

        return len(cubes_on)


def test_th_ch():
    """
    Run `python -m pytest ./day-22/part-1/th-ch.py` to test the submission.
    """
    assert (ThChSubmission().run("""
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682
""".strip()) == 590784)
