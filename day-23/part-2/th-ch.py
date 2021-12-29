from tool.runners.python import SubmissionPy

from functools import lru_cache
import heapq

energy_by_amphipod = {"A": 1, "B": 10, "C": 100, "D": 1000}


class Burrow():
    # array of [ None, "A", etc] with hallway from 0 to 10 and side rooms
    def __init__(self, burrow):
        self.burrow = burrow

    def __hash__(self):
        return hash(str(self.burrow))

    def __lt__(self, other):
        return True  # just for heapq, not actually used (energy is used for comparison)

    @lru_cache(maxsize=None)
    def is_organized(self):
        return self.__str__() == """
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########
"""

    @classmethod
    def parse(cls, s: str):
        string_indexes_to_positions = {
            (1, 1): 0,
            (1, 2): 1,
            (1, 3): 2,
            (1, 4): 3,
            (1, 5): 4,
            (1, 6): 5,
            (1, 7): 6,
            (1, 8): 7,
            (1, 9): 8,
            (1, 10): 9,
            (1, 11): 10,
            # Sideroom 1
            (2, 3): 11,
            (3, 3): 12,
            (4, 3): 13,
            (5, 3): 14,
            # Sideroom 2
            (2, 5): 15,
            (3, 5): 16,
            (4, 5): 17,
            (5, 5): 18,
            # Sideroom 3
            (2, 7): 19,
            (3, 7): 20,
            (4, 7): 21,
            (5, 7): 22,
            # Sideroom 4
            (2, 9): 23,
            (3, 9): 24,
            (4, 9): 25,
            (5, 9): 26,
        }
        burrow = [None] * 27
        lines = s.splitlines()
        for (i, j), burrow_position in string_indexes_to_positions.items():
            amphipod = lines[i][j]
            burrow[burrow_position] = None if amphipod == "." else amphipod
        return Burrow(tuple(burrow))

    @lru_cache(maxsize=None)
    def __str__(self):
        template = """
#############
#{i0}{i1}{i2}{i3}{i4}{i5}{i6}{i7}{i8}{i9}{i10}#
###{i11}#{i15}#{i19}#{i23}###
  #{i12}#{i16}#{i20}#{i24}#
  #{i13}#{i17}#{i21}#{i25}#
  #{i14}#{i18}#{i22}#{i26}#
  #########
"""
        values = {
            "i" + str(i): val or "."
            for i, val in enumerate(self.burrow)
        }
        return template.format(**values)


@lru_cache(maxsize=None)
def get_side_room(amphipod):
    if amphipod == "A":
        return [11, 12, 13, 14]
    elif amphipod == "B":
        return [15, 16, 17, 18]
    elif amphipod == "C":
        return [19, 20, 21, 22]
    elif amphipod == "D":
        return [23, 24, 25, 26]


@lru_cache(maxsize=None)
def get_space_next_to_sideroom(sideroom_entrance):
    if sideroom_entrance == 11:
        return 2
    elif sideroom_entrance == 15:
        return 4
    elif sideroom_entrance == 19:
        return 6
    else:
        return 8


forbidden = set([2, 4, 6, 8])


@lru_cache(maxsize=None)
def get_possible_positions(burrow_pos, position, amphipod):
    sideroom = get_side_room(amphipod)
    space_right_sideroom = get_space_next_to_sideroom(sideroom[0])

    # in the hallway - can only go into the right sideroom
    if position <= 10:
        if any(burrow_pos[i] is not None for i in range(
                min(position, space_right_sideroom) +
                1, max(position, space_right_sideroom))):
            return []

        if burrow_pos[sideroom[0]] is not None:
            return []

        if any(burrow_pos[i] is not None and burrow_pos[i] != amphipod
               for i in sideroom):
            return []

        i = 0
        while i < 4 and burrow_pos[sideroom[0] + i] is None:
            i += 1
        return [(sideroom[0] + i - 1, abs(position - space_right_sideroom) + i)
                ]

    # In a sideroom
    ################
    if position in sideroom:
        # Amphipod is in the right sideroom

        for pos in sideroom:
            if pos < position and burrow_pos[pos] is not None:
                # There is an amphipod on top: cannot move
                return []

        if all(a is None or a == amphipod for a in sideroom):
            # Only correct amphipods in the room: don't move
            return []

    # Amphipod can move into hallway or into the right sideroom
    top_of_side_room = 11 + 4 * ((position - 11) // 4)

    # Another amphipod on top: cannot move
    current_sideroom = range(top_of_side_room, top_of_side_room + 4)
    for pos in current_sideroom:
        if pos < position and burrow_pos[pos] is not None:
            return []

    space = get_space_next_to_sideroom(top_of_side_room)  # hallway space
    next_positions = []
    cost_to_go_out = 1 + (position - top_of_side_room)

    # Either the amphipod is not in the right
    # Can move into hallway or right sideroom

    # Try to move to left
    for i in range(space - 1, -1, -1):
        if burrow_pos[i] is not None:
            break
        if i not in forbidden:
            next_positions.append((i, abs(i - space) + cost_to_go_out))
        else:
            if i == space_right_sideroom:
                # Can only go there if empty or containing correct amphipods
                possible_pos = None
                for pos in sideroom:
                    if burrow_pos[pos] is None:
                        possible_pos = pos
                    elif burrow_pos[pos] != amphipod:
                        possible_pos = None
                        break
                if possible_pos is not None:
                    next_positions.append(
                        (possible_pos, cost_to_go_out + abs(i - space) + 1 +
                         (possible_pos - sideroom[0])))

    # Try to move to right
    for i in range(space + 1, 11):
        if burrow_pos[i] is not None:
            break
        if i not in forbidden:
            next_positions.append((i, abs(i - space) + cost_to_go_out))
        else:
            if i == space_right_sideroom:
                # Can only go there if empty or containing correct amphipods
                possible_pos = None
                for pos in sideroom:
                    if burrow_pos[pos] is None:
                        possible_pos = pos
                    elif burrow_pos[pos] != amphipod:
                        possible_pos = None
                        break
                if possible_pos is not None:
                    next_positions.append(
                        (possible_pos, cost_to_go_out + abs(i - space) + 1 +
                         (possible_pos - sideroom[0])))

    # Sort by smallest energy cost
    return sorted(next_positions, key=lambda next_position: next_position[1])


@lru_cache(maxsize=None)
def compute_next_burrows(burrow):
    next_burrows = []
    for position, amphipod in enumerate(burrow):
        if amphipod is None:
            continue

        next_positions = get_possible_positions(burrow, position, amphipod)
        for next_position, nb_moves in next_positions:
            new_burrow = list(burrow)[:]
            new_burrow[next_position], new_burrow[position] = new_burrow[
                position], None
            next_burrows.append(
                (tuple(new_burrow), nb_moves * energy_by_amphipod[amphipod]))

    return next_burrows


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        lines = s.splitlines()
        # Insert missing lines
        if len(lines) < 7:
            s = "\n".join(lines[:-2] + ["  #D#C#B#A#", "  #D#B#A#C#"] +
                          lines[-2:])
        queue = [(0, Burrow.parse(s))]
        heapq.heapify(queue)
        seen = {}

        while True:
            energy, burrow = heapq.heappop(queue)
            if burrow in seen and seen[burrow] < energy:
                continue

            if burrow.is_organized():
                return energy

            next_burrows = compute_next_burrows(burrow.burrow)
            for next_burrow, energy_cost in next_burrows:
                next_energy = energy + energy_cost
                if next_burrow in seen and seen[next_burrow] <= next_energy:
                    continue
                seen[next_burrow] = next_energy
                heapq.heappush(queue, (next_energy, Burrow(next_burrow)))


def test_th_ch():
    """
    Run `python -m pytest ./day-23/part-2/th-ch.py` to test the submission.
    """
    assert (ThChSubmission().run("""
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
""".strip()) == 44169)
