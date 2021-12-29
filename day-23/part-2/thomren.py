from itertools import product
from heapq import heappush, heappop
from typing import Iterator, List, Optional, Tuple

from tool.runners.python import SubmissionPy


TARGET = """
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########
""".strip()


class ThomrenSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        lines = s.splitlines()
        lines.insert(3, "  #D#C#B#A#")
        lines.insert(4, "  #D#B#A#C#")
        s = "\n".join(lines)

        start_state = State.from_str(s)
        target_state = State.from_str(TARGET)

        d, prev = a_star(start_state, target_state, get_neighbors, heuristic)

        state = target_state
        path = [state]
        while state != start_state:
            state = prev[state]
            path.append(state)

        for s in reversed(path):
            print(State.to_str(s))
            print()
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

        if len(prev) % 100000 == 0:
            print(len(prev))

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
            State.get_hallway(state, k) is None
            for k in range(min(j, t), max(j, t) + 1)
            if k != j
        ) and all(State.get_room(state, x, p) in [x, None] for p in range(4)):
            p = min(p for p in range(4) if State.get_room(state, x, p) is None)
            next_state = State.set_hallway(state, j, None)
            next_state = State.set_room(next_state, x, p, x)
            yield (next_state, (abs(j - t) + (4 - p)) * energy(x))

    # move amphipods out of the rooms
    for n in range(4):
        for pos in range(4):
            x = State.get_room(state, n, pos)

            if x is None:
                continue
            j = 2 * n + 2  # position of the current room in the hallway
            t = 2 * x + 2  # position of the target room in the hallway

            if x == n and all(State.get_room(state, n, p) == n for p in range(pos)):
                # the amphipod already is in its target position
                continue
            if any(State.get_room(state, n, p) is not None for p in range(pos + 1, 4)):
                # the amphipod is blocked by another one in the same room
                continue
            if State.get_hallway(state, 2 * n + 2) is not None:
                # the amphipod is blocked by another one in the hallway
                continue

            # go on the left in the hallway
            for k in range(1, j + 1):
                if State.get_hallway(state, j - k) is not None:
                    break

                # try to go into the target room
                if j - k == t and all(
                    State.get_room(state, x, p) in [x, None] for p in range(4)
                ):
                    p = min(p for p in range(4) if State.get_room(state, x, p) is None)
                    next_state = State.set_room(state, n, pos, None)
                    next_state = State.set_room(next_state, x, p, x)
                    yield (next_state, ((4 - pos) + k + (4 - p)) * energy(x))
                    continue  # not optimal not to go to the target room

                if j - k in [2, 4, 6, 8]:
                    # not optimal to stop in front of a room
                    continue

                next_state = State.set_room(state, n, pos, None)
                next_state = State.set_hallway(next_state, j - k, x)
                yield (next_state, ((4 - pos) + k) * energy(x))

            # go on the right in the hallway
            for k in range(1, 11 - j):
                if State.get_hallway(state, j + k) is not None:
                    break

                # try to go into the target room
                if j + k == t and all(
                    State.get_room(state, x, p) in [x, None] for p in range(4)
                ):
                    p = min(p for p in range(4) if State.get_room(state, x, p) is None)
                    next_state = State.set_room(state, n, pos, None)
                    next_state = State.set_room(next_state, x, p, x)
                    yield (next_state, ((4 - pos) + k + (4 - p)) * energy(x))
                    continue  # not optimal not to go to the target room

                if j + k in [2, 4, 6, 8]:
                    # not optimal to stop in front of a room
                    continue

                next_state = State.set_room(state, n, pos, None)
                next_state = State.set_hallway(next_state, j + k, x)
                yield (next_state, ((4 - pos) + k) * energy(x))


def heuristic(state):
    res = 0
    for j in range(11):
        if (x := State.get_hallway(state, j)) is not None:
            t = 2 * x + 2  # position of the target room in the hallway
            res += (1 + abs(j - t)) * energy(x)

    for n, pos in product(range(4), range(4)):
        if (x := State.get_room(state, n, pos)) is not None and x != n:
            res += (4 - pos + 2 * abs(x - n) + 1) * energy(x)
    return res


class State:
    # Class to manipulate the state represented by a 108-bit bitmask:
    # - each cell is represented by 4 bits indicating the presence of A, B, C and D
    # (from lower to higher bit, i.e. bit meanings are DCBA)
    # - the first 11 cells are the hallway from right to left
    # - the following 16 cells are the 4 rooms from right to left, bottom cell first
    # E.g.: target state bitmask =
    # 000000000000000000000000000000000000000000001000100010001000010001000100010000100010001000100001000100010001
    # |------------------------------------------||--------------||--------------||--------------||--------------|
    #                 Hallway                          Room 3          Room 2          Room 1          Room 0

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
        for i, j in product([1, 2, 3, 4], [2, 4, 6, 8]):
            if lines[i + 1][j + 1] in ["A", "B", "C", "D"]:
                x = ord(lines[i + 1][j + 1]) - ord("A")
                state = State.set_room(state, (j - 2) // 2, 4 - i, x)

        return state

    @staticmethod
    def to_str(state: int) -> str:
        lines = ["#" * 13]
        lines.append(
            f"#{''.join([State._int_to_char(State.get_hallway(state, i)) for i in range(11)])}#"
        )
        lines.append(
            f"###{'#'.join([State._int_to_char(State.get_room(state, n, 3)) for n in range(4)])}###"
        )
        for pos in reversed(range(3)):
            lines.append(
                f"  #{'#'.join([State._int_to_char(State.get_room(state, n, pos)) for n in range(4)])}#"
            )
        lines.append("  #########")
        return "\n".join(lines)

    @staticmethod
    def _int_to_char(x: Optional[int]) -> str:
        return "." if x is None else chr(ord("A") + x)

    @staticmethod
    def _hallway_cell_shift(idx: int) -> int:
        return 4 * (16 + idx)  # 8 is for the rooms

    @staticmethod
    def _room_cell_shift(n: int, pos: int) -> int:
        return 4 * (4 * n + pos)

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
        == 44169
    )


def test_state():
    states = [
        """
#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########
""".strip(),
        """
#############
#.....D.D.A.#
###.#B#C#.###
  #D#C#B#A#
  #D#B#A#C#
  #A#B#C#.#
  #########
""".strip(),
        """
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########
""".strip(),
    ]
    for s in states:
        assert State.to_str(State.from_str(s)) == s


SOL = """#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#..........D#
###B#C#B#.###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A.........D#
###B#C#B#.###
  #D#C#B#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A........BD#
###B#C#.#.###
  #D#C#B#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A......B.BD#
###B#C#.#.###
  #D#C#.#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#C#.#.###
  #D#C#.#.#
  #D#B#.#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#.#.#.###
  #D#C#.#.#
  #D#B#C#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#B#C#C#
  #A#D#C#A#
  #########

#############
#AA...B.B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#D#C#A#
  #########

#############
#AA.D.B.B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#.#C#A#
  #########

#############
#AA.D...B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#B#C#A#
  #########

#############
#AA.D.....BD#
###B#.#.#.###
  #D#.#C#.#
  #D#B#C#C#
  #A#B#C#A#
  #########

#############
#AA.D......D#
###B#.#.#.###
  #D#B#C#.#
  #D#B#C#C#
  #A#B#C#A#
  #########

#############
#AA.D......D#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#A#
  #########

#############
#AA.D.....AD#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#.#
  #########

#############
#AA.......AD#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#D#
  #########

#############
#AA.......AD#
###.#B#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#D#
  #########

#############
#AA.......AD#
###.#B#C#.###
  #.#B#C#.#
  #D#B#C#D#
  #A#B#C#D#
  #########

#############
#AA.D.....AD#
###.#B#C#.###
  #.#B#C#.#
  #.#B#C#D#
  #A#B#C#D#
  #########

#############
#A..D.....AD#
###.#B#C#.###
  #.#B#C#.#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#...D.....AD#
###.#B#C#.###
  #A#B#C#.#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#.........AD#
###.#B#C#.###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#..........D#
###A#B#C#.###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########"""


# def test_neighbors():
#     states = SOL.split("\n\n")
#     tot = 0
#     for i in range(len(states) - 1):
#         f = State.from_str(states[i])
#         t = State.from_str(states[i + 1])
#         if not any(s == t for s, d in get_neighbors(f)):
#             print(states[i])
#             print()
#             print(states[i + 1])
#         else:
#             dist = [d for s, d in get_neighbors(f) if s == t][0]
#             tot += dist
#             print(dist, tot)
#     assert False
