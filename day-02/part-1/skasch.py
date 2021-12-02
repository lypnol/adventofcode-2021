import enum
import dataclasses as dc
from typing import Iterable

from tool.runners.python import SubmissionPy


class Direction(enum.Enum):
    UP = "up"
    DOWN = "down"
    FORWARD = "forward"


@dc.dataclass
class Position:
    horizontal: int = 0
    depth: int = 0

    def move(self, direction: Direction, value: int) -> None:
        if direction == Direction.UP:
            self.depth -= value
        elif direction == Direction.DOWN:
            self.depth += value
        elif direction == Direction.FORWARD:
            self.horizontal += value
        else:
            raise ValueError(f"Unhandled direction {direction}")


class SkaschSubmission(SubmissionPy):

    def parse(self, s: str) -> Iterable[tuple[Direction, int]]:
        for line in s.splitlines():
            if stripped_line := line.strip():
                direction, value = stripped_line.split()
                yield Direction(direction), int(value)

    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        position = Position()
        for direction, value in self.parse(s):
            position.move(direction, value)
        return position.horizontal * position.depth


def test_skasch():
    """
    Run `python -m pytest ./day-02/part-1/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
forward 5
down 5
forward 8
up 3
down 8
forward 2
""".strip()
        )
        == 150
    )
