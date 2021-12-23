import dataclasses as dc
import functools
import heapq
import re
from typing import Dict, Iterable, NamedTuple, Set

from tool.runners.python import SubmissionPy

REGEX1 = re.compile(r"###([A-D])#([A-D])#([A-D])#([A-D])###")
REGEX2 = re.compile(r"  #([A-D])#([A-D])#([A-D])#([A-D])#")
MAX_Y = 2


class Pos(NamedTuple):
    x: int
    y: int

    def dist(self, other: "Pos") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __str__(self) -> str:
        return f"{self.x}{self.y}"


HALLS = {Pos(x, 0) for x in (0, 1, 3, 5, 7, 9, 10)}
ROOMS = {Pos(x, y) for x in (2, 4, 6, 8) for y in range(1, MAX_Y + 1)}
X_BY_AMPHIPOD = {"A": 2, "B": 4, "C": 6, "D": 8}


@functools.lru_cache(None)
def get_path(pos1: Pos, pos2: Pos) -> Set[Pos]:
    res = set()
    if pos1.y == 0:
        for x in range(pos2.x, pos1.x, 1 if pos1.x >= pos2.x else -1):
            res.add(Pos(x, 0))
        for y in range(pos2.y + 1):
            res.add(Pos(pos2.x, y))
        return res
    else:
        for y in range(pos1.y):
            res.add(Pos(pos1.x, y))
        min_x, max_x = sorted([pos1.x, pos2.x])
        for x in range(min_x, max_x + 1):
            res.add(Pos(x, 0))
        return res


Positions = Dict[Pos, str]

COST = {"A": 1, "B": 10, "C": 100, "D": 1000}


def parse(s: str) -> Positions:
    lines = s.splitlines()
    m1 = REGEX1.match(lines[2])
    assert m1 is not None
    m2 = REGEX2.match(lines[3])
    assert m2 is not None
    return {
        Pos(2, 1): m1.group(1),
        Pos(4, 1): m1.group(2),
        Pos(6, 1): m1.group(3),
        Pos(8, 1): m1.group(4),
        Pos(2, 2): m2.group(1),
        Pos(4, 2): m2.group(2),
        Pos(6, 2): m2.group(3),
        Pos(8, 2): m2.group(4),
    }


TARGET_POSITIONS = {Pos(x, y): amphipod for amphipod, x in X_BY_AMPHIPOD.items() for y in range(1, MAX_Y + 1)}


@dc.dataclass
class State:
    energy: int
    positions: Positions

    def __le__(self, other: "State") -> bool:
        return self.energy <= other.energy

    def __lt__(self, other: "State") -> bool:
        return self.energy < other.energy

    def positions_str(self) -> str:
        return "".join(f"{pos}{amphipod}" for pos, amphipod in sorted(self.positions.items()))

    def display(self) -> str:
        grid = [
            list("#############{}"),
            list("#...........#"),
            list("###.#.#.#.###"),
            list("  #.#.#.#.#"),
            list("  #########"),
        ]
        for pos, amphipod in self.positions.items():
            grid[pos.y + 1][pos.x + 1] = amphipod
        return "\n".join("".join(row) for row in grid).format(f" Energy: {self.energy}")


def next_moves(state: State) -> Iterable[State]:
    state_pos = set(state.positions)
    for pos, amphipod in state.positions.items():
        base_state = {p: a for p, a in state.positions.items() if p != pos}
        if pos in ROOMS:
            if pos.x == X_BY_AMPHIPOD[amphipod]:
                if any(
                    pos.y == y
                    and all(state.positions.get(Pos(pos.x, yy)) == amphipod for yy in range(y + 1, MAX_Y + 1))
                    for y in range(1, MAX_Y + 1)
                ):
                    continue
            for target in HALLS:
                path = get_path(pos, target)  # type: ignore
                if path & state_pos:
                    continue
                yield State(state.energy + COST[amphipod] * pos.dist(target), {target: amphipod, **base_state})
        elif pos in HALLS:
            target_x = X_BY_AMPHIPOD[amphipod]
            target = None
            for y in range(MAX_Y, 0, -1):
                next_amphipod = state.positions.get(Pos(target_x, y))
                if next_amphipod == amphipod:
                    continue
                elif next_amphipod is None:
                    if all(Pos(target_x, yy) not in state.positions for yy in range(1, y)):
                        target = Pos(target_x, y)
                        break
                else:
                    break
            if target is None:
                continue
            path = get_path(pos, target)  # type: ignore
            if path & state_pos:
                continue
            yield State(state.energy + COST[amphipod] * pos.dist(target), {target: amphipod, **base_state})


class SkaschSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        positions = parse(s)
        q = [State(0, positions)]
        visited = set()
        while True:
            state = heapq.heappop(q)
            positions_str = state.positions_str()
            if positions_str in visited:
                continue
            visited.add(positions_str)
            if state.positions == TARGET_POSITIONS:
                return state.energy
            for next_state in next_moves(state):
                if next_state.positions_str() in visited:
                    continue
                heapq.heappush(q, next_state)


def test_skasch() -> None:
    """
    Run `python -m pytest ./day-23/part-1/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
""".strip()
        )
        == 12521
    )
