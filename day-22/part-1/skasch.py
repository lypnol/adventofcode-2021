import re
from typing import Iterable, List, NamedTuple, Optional, Tuple

from tool.runners.python import SubmissionPy


class Cube(NamedTuple):
    x0: int
    x1: int
    y0: int
    y1: int
    z0: int
    z1: int

    def __repr__(self) -> str:
        return f"Cube({self.x0}..{self.x1},{self.y0}..{self.y1},{self.z0}..{self.z1})"


REGEX = re.compile(
    r"(on|off) "
    r"x=(-?[0-9]+)..(-?[0-9]+),y=(-?[0-9]+)..(-?[0-9]+),z=(-?[0-9]+)..(-?[0-9]+)"
)


def parse(s: str) -> Iterable[Tuple[bool, Cube]]:
    for line in s.splitlines():
        if (m := REGEX.match(line.strip())) is not None:
            yield m.group(1) == "on", Cube(
                int(m.group(2)),
                int(m.group(3)),
                int(m.group(4)),
                int(m.group(5)),
                int(m.group(6)),
                int(m.group(7)),
            )


def volume(cube: Cube) -> int:
    return (cube.x1 - cube.x0 + 1) * (cube.y1 - cube.y0 + 1) * (cube.z1 - cube.z0 + 1)


def intersect(cube1: Cube, cube2: Cube) -> Optional[Cube]:
    (_, xl1), (xh0, xh1) = sorted([(cube1.x0, cube1.x1), (cube2.x0, cube2.x1)])
    if xl1 < xh0:
        return None
    (_, yl1), (yh0, yh1) = sorted([(cube1.y0, cube1.y1), (cube2.y0, cube2.y1)])
    if yl1 < yh0:
        return None
    (_, zl1), (zh0, zh1) = sorted([(cube1.z0, cube1.z1), (cube2.z0, cube2.z1)])
    if zl1 < zh0:
        return None
    return Cube(xh0, min(xl1, xh1), yh0, min(yl1, yh1), zh0, min(zl1, zh1))


INIT_BOUNDS = 50


class SkaschSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        cubes: List[Tuple[Cube, int]] = []
        for on, cube in parse(s):
            if any(abs(coord) > INIT_BOUNDS for coord in cube):
                continue
            new_cubes: List[Tuple[Cube, int]] = [(cube, 1)] if on else []
            for prev_cube, val in cubes:
                if (intersection := intersect(cube, prev_cube)) is not None:
                    new_cubes.append((intersection, -val))
            cubes.extend(new_cubes)
        return sum(val * volume(cube) for cube, val in cubes)


def test_skasch() -> None:
    """
    Run `python -m pytest ./day-22/part-1/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
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
""".strip()
        )
        == 590784
    )
