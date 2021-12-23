import dataclasses as dc
import functools
import heapq
import re
from typing import Dict, Iterable, Tuple

from tool.runners.python import SubmissionPy

REGEX1 = re.compile(r"###([A-D])#([A-D])#([A-D])#([A-D])###")
REGEX2 = re.compile(r"  #([A-D])#([A-D])#([A-D])#([A-D])#")
HALL_PATHS = (
    ([3, 5, 7, 9, 10], [1, 0]),
    ([5, 7, 9, 10], [3, 1, 0]),
    ([7, 9, 10], [5, 3, 1, 0]),
    ([9, 10], [7, 5, 3, 1, 0]),
)
MAX_Y = 4
AMPHIPODS = "ABCD"
TARGET_ROOM = {"A": 0, "B": 1, "C": 2, "D": 3}
ROOM_X = [2, 4, 6, 8]
HALLS_POS = [0, 1, 3, 5, 7, 9, 10]


HallsState = Dict[int, str]
RoomsState = Tuple[str, str, str, str]


@dc.dataclass
class State:
    energy: int
    halls: HallsState
    rooms: RoomsState
    green: Tuple[bool, bool, bool, bool] = (False, False, False, False)

    def __le__(self, other: "State") -> bool:
        return self.energy <= other.energy

    def __lt__(self, other: "State") -> bool:
        return self.energy < other.energy

    def positions_str(self) -> str:
        a = "".join(self.halls.get(pos, ".") for pos in HALLS_POS)
        b = "|".join(self.rooms)
        return f"{a}{b}"

    def display(self) -> str:
        grid = [
            list("#############{}"),
            list("#...........#"),
            list("###.#.#.#.###"),
            list("  #.#.#.#.#"),
            list("  #.#.#.#.#"),
            list("  #.#.#.#.#"),
            list("  #########"),
        ]
        for pos, amphipod in self.halls.items():
            grid[1][pos + 1] = amphipod
        for xr, room in enumerate(self.rooms):
            for dy, amphipod in enumerate(room):
                grid[MAX_Y + 1 - dy][3 + 2 * xr] = amphipod
        return "\n".join("".join(row) for row in grid).format(f" Energy: {self.energy}")


COST = {"A": 1, "B": 10, "C": 100, "D": 1000}


def parse(s: str) -> Tuple[HallsState, RoomsState]:
    lines = s.splitlines()
    m1 = REGEX1.match(lines[2])
    assert m1 is not None
    m2 = REGEX2.match(lines[3])
    assert m2 is not None
    return {}, (
        f"{m2.group(1)}DD{m1.group(1)}",
        f"{m2.group(2)}BC{m1.group(2)}",
        f"{m2.group(3)}AB{m1.group(3)}",
        f"{m2.group(4)}CA{m1.group(4)}",
    )


def is_valid(rooms: RoomsState) -> bool:
    return all(
        len(room) == MAX_Y and all(amphipod == target for amphipod in room) for room, target in zip(rooms, AMPHIPODS)
    )


@functools.lru_cache(None)
def dist(hall_pos: int, room_x: int, room_size: int) -> int:
    return abs(room_x - hall_pos) + (MAX_Y - room_size)


@functools.lru_cache(None)
def replace_room(rooms: RoomsState, next_room: Tuple[str, ...], room_idx: int) -> RoomsState:
    return rooms[:room_idx] + (next_room,) + rooms[room_idx + 1 :]  # type: ignore


@functools.lru_cache(None)
def green_light(green: Tuple[bool, bool, bool, bool], new_idx: int) -> Tuple[bool, bool, bool, bool]:
    return green[:new_idx] + (True,) + green[new_idx + 1 :]  # type: ignore


def next_moves(state: State) -> Iterable[State]:
    room_halls = set(state.halls) & {1, 3, 5, 7, 9}
    for room_idx, room in enumerate(state.rooms):
        if state.green[room_idx]:
            continue
        if not room:
            continue
        amphipod = room[-1]
        next_room = room[:-1]
        x = ROOM_X[room_idx]
        new_green = state.green
        if not state.green[room_idx] and all(a == AMPHIPODS[room_idx] for a in next_room):
            new_green = green_light(new_green, room_idx)
        for target in HALL_PATHS[room_idx][0]:
            if target in state.halls:
                break
            yield State(
                state.energy + COST[amphipod] * dist(target, x, len(next_room)),
                {**state.halls, target: amphipod},
                replace_room(state.rooms, next_room, room_idx),
                new_green,
            )
        for target in HALL_PATHS[room_idx][1]:
            if target in state.halls:
                break
            yield State(
                state.energy + COST[amphipod] * dist(target, x, len(next_room)),
                {**state.halls, target: amphipod},
                replace_room(state.rooms, next_room, room_idx),
                new_green,
            )
    for hall, amphipod in state.halls.items():
        target_room_idx = TARGET_ROOM[amphipod]
        if not state.green[target_room_idx]:
            continue
        target = ROOM_X[target_room_idx]
        left, right = sorted([hall, target])
        if any(left < h < right for h in room_halls):
            continue
        next_room = state.rooms[target_room_idx] + amphipod
        yield State(
            state.energy + COST[amphipod] * dist(hall, target, len(state.rooms[target_room_idx])),
            {h: a for h, a in state.halls.items() if h != hall},
            replace_room(state.rooms, next_room, target_room_idx),
            green_light(state.green, target_room_idx),
        )


class SkaschSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        halls, rooms = parse(s)
        q = [State(0, halls, rooms)]
        visited = {q[0].positions_str(): 0}
        while True:
            state = heapq.heappop(q)
            positions_str = state.positions_str()
            if positions_str in visited and state.energy > visited[positions_str]:
                continue
            if is_valid(state.rooms):
                return state.energy
            for next_state in next_moves(state):
                position_str = next_state.positions_str()
                if position_str in visited and visited[position_str] <= next_state.energy:
                    continue
                visited[position_str] = next_state.energy
                heapq.heappush(q, next_state)


def test_skasch() -> None:
    """
    Run `python -m pytest ./day-23/part-2/skasch.py` to test the submission.
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
        == 44169
    )
