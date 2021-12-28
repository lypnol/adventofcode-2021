from copy import deepcopy
from itertools import product
from heapq import heappush, heappop
from random import random
from typing import Iterator, List, Optional, Tuple

from tool.runners.python import SubmissionPy


TARGET = """
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
""".strip()


class ThomrenSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        start_state = State.from_str(s)
        target_state = State.from_str(TARGET)

        d, _ = a_star(start_state, target_state, get_neighbors, heuristic)
        return d


def energy(x):
    return 10 ** x


def a_star(start, end, get_neighbors, heuristic):
    frontier = [(heuristic(start), 0, start, None)]
    min_in_heap_by_state = {}
    prev = {}

    while len(frontier) > 0:
        (h, dist, state, prev_state) = heappop(frontier)

        if state in prev:
            continue
        prev[state] = prev_state

        if state == end:
            return dist, prev

        for (s, d) in get_neighbors(state):
            h = heuristic(s) + dist + d
            if s not in min_in_heap_by_state or h <= min_in_heap_by_state[s]:
                heappush(frontier, (h, dist + d, s, state))
                min_in_heap_by_state[s] = h

    return -1, prev


def get_neighbors(state: int) -> Iterator[Tuple[int, int]]:
    # try to move amphipods in the hallway to their room
    for j in range(11):
        x = State.get_hallway(state, j)
        if x is None:
            continue
        t = 2 * x + 2  # position of the target room in the hallway

        if all(
            y is None
            for y in (
                [
                    State.get_hallway(state, k)
                    for k in range(min(j, t), max(j, t))
                    if k != j
                ]
                + [State.get_room(state, x, 0), State.get_room(state, x, 1)]
            )
        ):
            next_state = State.set_hallway(state, j, None)
            next_state = State.set_room(next_state, x, 0, x)
            yield (next_state, (abs(j - t) + 2) * energy(x))
        elif (
            all(
                y is None
                for y in (
                    [
                        State.get_hallway(state, k)
                        for k in range(min(j, t), max(j, t))
                        if k != j
                    ]
                    + [State.get_room(state, x, 1)]
                )
            )
            and State.get_room(state, x, 0) == x
        ):
            next_state = State.set_hallway(state, j, None)
            next_state = State.set_room(next_state, x, 1, x)
            yield (next_state, (abs(j - t) + 1) * energy(x))

    # move amphipods out of the rooms
    for n in range(4):
        for pos in range(2):
            x = State.get_room(state, n, pos)

            if x is None:
                continue
            j = 2 * n + 2  # position of the current room in the hallway
            t = 2 * x + 2  # position of the target room in the hallway

            if x == n and (pos == 0 or State.get_room(state, n, 0) == n):
                # the amphipod already is in its target position
                continue
            if pos == 0 and State.get_room(state, n, 1) is not None:
                # the amphipod is blocked by another one in the same room
                continue
            if State.get_hallway(state, 2 * n + 2) is not None:
                # the amphipod is blocked by another one in the hallway
                continue

            # go on the left in the hallway
            for p in range(1, j + 1):
                if State.get_hallway(state, j - p) is not None:
                    break

                next_state = State.set_room(state, n, pos, None)
                next_state = State.set_hallway(next_state, j - p, x)
                yield (next_state, ((2 - pos) + p) * energy(x))

                # try to go into the target room
                # TODO: continue if can go to target room?
                if j - p == t:
                    if (
                        State.get_room(state, x, 1) is None
                        and State.get_room(state, x, 0) is None
                    ):
                        next_state = State.set_room(state, n, pos, None)
                        next_state = State.set_room(next_state, x, 0, x)
                        yield (next_state, ((2 - pos) + p + 2) * energy(x))
                    elif (
                        State.get_room(state, x, 1) is None
                        and State.get_room(state, x, 0) == x
                    ):
                        next_state = State.set_room(state, n, pos, None)
                        next_state = State.set_room(next_state, x, 1, x)
                        yield (next_state, ((2 - pos) + p + 1) * energy(x))

            # go on the right in the hallway
            for p in range(1, 11 - j):
                if State.get_hallway(state, j + p) is not None:
                    break

                next_state = State.set_room(state, n, pos, None)
                next_state = State.set_hallway(next_state, j + p, x)
                yield (next_state, ((2 - pos) + p) * energy(x))

                # try to go into the target room
                # TODO: continue if can go to target room?
                if j + p == t:
                    if (
                        State.get_room(state, x, 1) is None
                        and State.get_room(state, x, 0) is None
                    ):
                        next_state = State.set_room(state, n, pos, None)
                        next_state = State.set_room(next_state, x, 0, x)
                        yield (next_state, ((2 - pos) + p + 2) * energy(x))
                    elif (
                        State.get_room(state, x, 1) is None
                        and State.get_room(state, x, 0) == x
                    ):
                        next_state = State.set_room(state, n, pos, None)
                        next_state = State.set_room(next_state, x, 1, x)
                        yield (next_state, ((2 - pos) + p + 1) * energy(x))


def heuristic(state):
    res = 0
    for j in range(11):
        if (x := State.get_hallway(state, j)) is not None:
            t = 2 * x + 2  # position of the target room in the hallway
            res += (1 + abs(j - t)) * energy(x)

    for n, pos in product(range(4), range(2)):
        if (x := State.get_hallway(state, j)) is not None and x != n:
            res += (2 - pos + 2 * abs(x - n) + 1) * energy(x)
    return res


class State:
    # Class to manipulate the state represented by a 76-bit bitmask:
    # - each cell is represented by 4 bits indicating the presence of A, B, C and D
    # (from lower to higher bit, i.e. bit meanings are DCBA)
    # - the first 11 cells are the hallway from right to left
    # - the following 8 cells are the 4 rooms from right to left, bottom cell first
    # E.g.: target state bitmask =
    # 0000000000000000000000000000000000000000000000010001001000100100010010001000
    # |------------------------------------------||------||------||------||------|
    #                 Hallway                      Room 3  Room 2  Room 1  Room 0

    @staticmethod
    def from_str(s: str) -> int:
        state = 0
        lines = s.splitlines()

        # hallway
        for j, c in enumerate(lines[1][1:-1]):
            if c in ["A", "B", "C", "D"]:
                x = ord(c) - ord("A")
                state = State.set_hallway(state, j, x)

        # rooms
        for i, j in product([1, 2], [2, 4, 6, 8]):
            if lines[i + 1][j + 1] in ["A", "B", "C", "D"]:
                x = ord(lines[i + 1][j + 1]) - ord("A")
                state = State.set_room(state, (j - 2) // 2, 2 - i, x)

        return state

    @staticmethod
    def to_str(state: int) -> str:
        lines = ["#" * 13]
        lines.append(
            f"#{''.join([State._int_to_char(State.get_hallway(state, i)) for i in range(11)])}#"
        )
        lines.append(
            f"###{'#'.join([State._int_to_char(State.get_room(state, n, 1)) for n in range(4)])}###"
        )
        lines.append(
            f"  #{'#'.join([State._int_to_char(State.get_room(state, n, 0)) for n in range(4)])}#"
        )
        lines.append("  #########")
        return "\n".join(lines)

    @staticmethod
    def _int_to_char(x: Optional[int]) -> str:
        return "." if x is None else chr(ord("A") + x)

    @staticmethod
    def _hallway_cell_shift(idx: int) -> int:
        return 4 * (8 + idx)  # 8 is for the rooms

    @staticmethod
    def _room_cell_shift(n: int, pos: int) -> int:
        return 4 * (2 * n + pos)

    @staticmethod
    def get_hallway(state: int, idx: int) -> Optional[int]:
        shift = State._hallway_cell_shift(idx)
        cell = (state & ((0b1111) << shift)) >> shift

        if cell == 0:
            return None
        return cell.bit_length() - 1

    @staticmethod
    def get_room(state: int, n: int, pos: int) -> Optional[int]:
        shift = State._room_cell_shift(n, pos)
        cell = (state & ((0b1111) << shift)) >> shift
        if cell == 0:
            return None
        return cell.bit_length() - 1

    @staticmethod
    def set_hallway(state: int, idx: int, x: Optional[int]) -> int:
        if x is not None:
            state |= 1 << (State._hallway_cell_shift(idx) + x)
        else:
            state &= ~((0b1111) << State._hallway_cell_shift(idx))
        return state

    @staticmethod
    def set_room(state: int, n: int, pos: int, x: Optional[int]) -> int:
        if x is not None:
            state |= 1 << (State._room_cell_shift(n, pos) + x)
        else:
            state &= ~((0b1111) << State._room_cell_shift(n, pos))
        return state


def test_thomren():
    """
    Run `python -m pytest ./day-23/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
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


def test_state():
    states = [
        """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
""".strip(),
        """
#############
#.....D.D.A.#
###.#B#C#.###
  #A#B#C#.#
  #########
""".strip(),
        """
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
""".strip(),
    ]
    for s in states:
        assert State.to_str(State.from_str(s)) == s
