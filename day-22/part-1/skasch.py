import dataclasses as dc
import re
from typing import Iterable, List, Optional, Tuple

from tool.runners.python import SubmissionPy

Cube = Tuple[int, int, int, int, int, int]

REGEX = re.compile(
    r"(on|off) "
    r"x=(-?[0-9]+)..(-?[0-9]+),y=(-?[0-9]+)..(-?[0-9]+),z=(-?[0-9]+)..(-?[0-9]+)"
)


def parse(s: str) -> Iterable[Tuple[bool, Cube]]:
    for line in s.splitlines():
        if (m := REGEX.match(line.strip())) is not None:
            yield m.group(1) == "on", (
                int(m.group(2)),
                int(m.group(3)),
                int(m.group(4)),
                int(m.group(5)),
                int(m.group(6)),
                int(m.group(7)),
            )


def volume(cube: Cube) -> int:
    return (cube[1] - cube[0] + 1) * (cube[3] - cube[2] + 1) * (cube[5] - cube[4] + 1)


def intersect(cube1: Cube, cube2: Cube) -> Optional[Cube]:
    xl1, xh0, xh1 = (
        (cube1[1], cube2[0], cube2[1])
        if cube1[0] <= cube2[0]
        else (cube2[1], cube1[0], cube1[1])
    )
    if xl1 < xh0:
        return None
    yl1, yh0, yh1 = (
        (cube1[3], cube2[2], cube2[3])
        if cube1[2] <= cube2[2]
        else (cube2[3], cube1[2], cube1[3])
    )
    if yl1 < yh0:
        return None
    zl1, zh0, zh1 = (
        (cube1[5], cube2[4], cube2[5])
        if cube1[4] <= cube2[4]
        else (cube2[5], cube1[4], cube1[5])
    )
    if zl1 < zh0:
        return None
    return (xh0, min(xl1, xh1), yh0, min(yl1, yh1), zh0, min(zl1, zh1))


@dc.dataclass
class ValuedCube:
    cube: Cube
    val: int


INIT_BOUNDS = 50


class SkaschSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        cubes: List[ValuedCube] = []
        for on, cube in parse(s):
            if any(abs(coord) > INIT_BOUNDS for coord in cube):
                continue
            new_cubes: List[ValuedCube] = [ValuedCube(cube, 1)] if on else []
            remove_cubes = []
            for idx, valued_cube in enumerate(cubes):
                if (intersection := intersect(cube, valued_cube.cube)) is not None:
                    if intersection == valued_cube.cube:
                        remove_cubes.append(idx)
                    elif on and intersection == cube:
                        new_cubes[0].val -= valued_cube.val
                    else:
                        new_cubes.append(ValuedCube(intersection, -valued_cube.val))
            for idx in reversed(remove_cubes):
                del cubes[idx]
            cubes.extend(new_cubes)
        return sum(valued_cube.val * volume(valued_cube.cube) for valued_cube in cubes)


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
