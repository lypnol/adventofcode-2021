from tool.runners.python import SubmissionPy

from functools import lru_cache
import heapq

energy_by_amphipod = {"A": 1, "B": 10, "C": 100, "D": 1000}


class Burrow():
    # array of [ None, "A", etc] with hallway from 0 to 10 and side rooms:
    # 11 13 15 17
    # 12 14 16 18
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
            (2, 3): 11,
            (3, 3): 12,
            (2, 5): 13,
            (3, 5): 14,
            (2, 7): 15,
            (3, 7): 16,
            (2, 9): 17,
            (3, 9): 18,
        }
        burrow = [None] * 19
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
###{i11}#{i13}#{i15}#{i17}###
  #{i12}#{i14}#{i16}#{i18}#
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
        return [11, 12]
    elif amphipod == "B":
        return [13, 14]
    elif amphipod == "C":
        return [15, 16]
    elif amphipod == "D":
        return [17, 18]


forbidden = set([2, 4, 6, 8])


@lru_cache(maxsize=None)
def get_possible_positions(burrow_pos, position, amphipod):
    sideroom = get_side_room(amphipod)
    space_right_sideroom = sideroom[0] - 9

    # in the hallway
    if position <= 10:
        if any(burrow_pos[i] is not None for i in range(
                min(position, space_right_sideroom) +
                1, max(position, space_right_sideroom))):
            return []

        if burrow_pos[sideroom[0]] is not None:
            return []
        if burrow_pos[sideroom[1]] is not None:
            if burrow_pos[sideroom[1]] != amphipod:
                return []
            else:
                return [(sideroom[0], abs(position - space_right_sideroom) + 1)
                        ]
        return [(sideroom[1], abs(position - space_right_sideroom) + 2)]

    bottom_of_side_room = position if position % 2 == 0 else position + 1
    top_of_side_room = bottom_of_side_room - 1

    # In a sideroom
    if position == sideroom[1] or (position == sideroom[0]
                                   and burrow_pos[sideroom[1]] == amphipod):
        # In the right sideroom: don't move
        return []

    # In a wrong sideroom

    if position == bottom_of_side_room and burrow_pos[
            top_of_side_room] is not None:
        return []

    # in top of sideroom: can go in hallway or right sideroom
    space = top_of_side_room - 9  # hallway space
    next_positions = []
    cost_to_go_out = 1 + (1 if position == bottom_of_side_room else 0)
    # Try to move to left
    for i in range(space - 1, -1, -1):
        if burrow_pos[i] is not None:
            break
        if i not in forbidden:
            next_positions.append((i, abs(i - space) + cost_to_go_out))
        else:
            if i == space_right_sideroom:
                if burrow_pos[sideroom[0]] is None:
                    if burrow_pos[sideroom[1]] is None:
                        next_positions.append(
                            (sideroom[1], abs(i - space) + cost_to_go_out + 2))
                    elif burrow_pos[sideroom[1]] == amphipod:
                        next_positions.append(
                            (sideroom[0], abs(i - space) + cost_to_go_out + 1))

    # Try to move to right
    for i in range(space + 1, 11):
        if burrow_pos[i] is not None:
            break
        if i not in forbidden:
            next_positions.append((i, abs(i - space) + cost_to_go_out))
        else:
            if i == space_right_sideroom:
                if burrow_pos[sideroom[0]] is None:
                    if burrow_pos[sideroom[1]] is None:
                        next_positions.append(
                            (sideroom[1], abs(i - space) + cost_to_go_out + 2))
                    elif burrow_pos[sideroom[1]] == amphipod:
                        next_positions.append(
                            (sideroom[0], abs(i - space) + cost_to_go_out + 1))

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
    Run `python -m pytest ./day-23/part-1/th-ch.py` to test the submission.
    """
    assert (ThChSubmission().run("""
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
""".strip()) == 12521)
