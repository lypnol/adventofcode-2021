from typing import Callable, Iterator, Tuple
from tool.runners.python import SubmissionPy


class SkaschSubmission(SubmissionPy):

    def parse(self, s: str) -> Iterator[str]:
        for line in s.splitlines():
            if stripped_line := line.strip():
                yield stripped_line

    def split(
        self, lines: Iterator[str], filter: Callable[[str], bool] = lambda l: l[0] == "1"
    ) -> Tuple[list[str], list[str]]:
        falsy, truthy = [], []
        for line in lines:
            if filter(line):
                truthy.append(line)
            else:
                falsy.append(line)
        return falsy, truthy

    def find(self, values: list[str], most_common: bool, equality_char: str) -> int:
        """This function modifies values inplace."""
        idx = 1
        while len(values) > 1:
            count = sum(value[idx] == "1" for value in values)
            if 2 * count == len(values):
                values = [value for value in values if value[idx] == equality_char]
            elif (2 * count > len(values)) == most_common:
                values = [value for value in values if value[idx] == "1"]
            else:
                values = [value for value in values if value[idx] == "0"]
            idx += 1
        return int(values[0], 2)

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        zeros_data, ones_data = self.split(self.parse(s))
        if len(zeros_data) > len(ones_data):
            o2_generator_data, co2_scrubber_data = zeros_data, ones_data
        else:
            co2_scrubber_data, o2_generator_data = zeros_data, ones_data
        o2_generator_rating = self.find(o2_generator_data, True, "1")
        co2_scrubber_rating = self.find(co2_scrubber_data, False, "0")
        return o2_generator_rating * co2_scrubber_rating


def test_skasch():
    """
    Run `python -m pytest ./day-03/part-2/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
""".strip()
        )
        == 230
    )
