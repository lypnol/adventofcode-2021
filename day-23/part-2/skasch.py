import dataclasses as dc
import functools
import heapq
import re
from typing import Dict, Iterable, List, Tuple

from tool.runners.python import SubmissionPy

REGEX1 = re.compile(r"###([A-D])#([A-D])#([A-D])#([A-D])###")
REGEX2 = re.compile(r"  #([A-D])#([A-D])#([A-D])#([A-D])#")
HALLS = {0, 1, 3, 5, 7, 9, 10}
MAX_Y = 4
AMPHIPODS = "ABCD"
TARGET_ROOM = {"A": 0, "B": 1, "C": 2, "D": 3}
ROOM_X = [2, 4, 6, 8]


@functools.lru_cache(None)
def dist(hall_pos: int, room_x: int, room_size: int) -> int:
    return abs(room_x - hall_pos) + (MAX_Y - room_size)


HallsState = Dict[int, str]
RoomsState = Tuple[List[str], List[str], List[str], List[str]]

COST = {"A": 1, "B": 10, "C": 100, "D": 1000}


def is_valid(rooms: RoomsState) -> bool:
    return all(
        len(room) == MAX_Y and all(amphipod == target for amphipod in room) for room, target in zip(rooms, AMPHIPODS)
    )


def parse(s: str) -> Tuple[HallsState, RoomsState]:
    lines = s.splitlines()
    m1 = REGEX1.match(lines[2])
    assert m1 is not None
    m2 = REGEX2.match(lines[3])
    assert m2 is not None
    return {}, (
        [m2.group(1), "D", "D", m1.group(1)],
        [m2.group(2), "B", "C", m1.group(2)],
        [m2.group(3), "A", "B", m1.group(3)],
        [m2.group(4), "C", "A", m1.group(4)],
    )


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
        halls_str = "".join(f"{pos}{amphipod}" for pos, amphipod in sorted(self.halls.items()))
        rooms_str = "|".join("".join(room) for room in self.rooms)
        return f"{halls_str}.{rooms_str}"

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


def replace_room(rooms: RoomsState, next_room: List[str], room_idx: int) -> RoomsState:
    if room_idx == 0:
        return next_room, rooms[1], rooms[2], rooms[3]
    elif room_idx == 1:
        return rooms[0], next_room, rooms[2], rooms[3]
    elif room_idx == 2:
        return rooms[0], rooms[1], next_room, rooms[3]
    else:
        return rooms[0], rooms[1], rooms[2], next_room


@functools.lru_cache(None)
def green_light(green: Tuple[bool, bool, bool, bool], new_idx: int) -> Tuple[bool, bool, bool, bool]:
    if new_idx == 0:
        return True, green[1], green[2], green[3]
    elif new_idx == 1:
        return green[0], True, green[2], green[3]
    elif new_idx == 2:
        return green[0], green[1], True, green[3]
    else:
        return green[0], green[1], green[2], True


def next_moves(state: State) -> Iterable[State]:
    free_halls = HALLS - set(state.halls)
    for room_idx, room in enumerate(state.rooms):
        if state.green[room_idx]:
            continue
        if not room:
            continue
        amphipod = room[-1]
        next_room = room[:-1]
        x = ROOM_X[room_idx]
        new_green = state.green
        if all(a == AMPHIPODS[room_idx] for a in next_room):
            new_green = green_light(new_green, room_idx)
        for target in free_halls:
            if any((hall - x) * (target - hall) > 0 for hall in state.halls):
                continue
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
        if any((other_hall - hall) * (target - other_hall) > 0 for other_hall in state.halls if other_hall != hall):
            continue
        next_room = state.rooms[target_room_idx] + [amphipod]
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
        visited = {q[0].positions_str()}
        while True:
            state = heapq.heappop(q)
            if is_valid(state.rooms):
                return state.energy
            for next_state in next_moves(state):
                positions_str = next_state.positions_str()
                if positions_str in visited:
                    continue
                visited.add(positions_str)
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
