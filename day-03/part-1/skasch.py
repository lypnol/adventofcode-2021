from typing import Iterator
from tool.runners.python import SubmissionPy


class SkaschSubmission(SubmissionPy):

    def parse(self, s: str) -> Iterator[str]:
        for line in s.splitlines():
            if stripped_line := line.strip():
                yield stripped_line

    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        counter = None
        n_lines = 0
        for line in self.parse(s):
            if counter is None:
                counter = [0] * len(line)
            n_lines += 1
            for idx, char in enumerate(line):
                if char == "1":
                    counter[idx] += 1
        gamma = 0
        epsilon = 0
        for count in counter:
            gamma = gamma * 2 + (2 * count > n_lines)
            epsilon = epsilon * 2 + (2 * count <= n_lines)
        return gamma * epsilon



def test_skasch():
    """
    Run `python -m pytest ./day-03/part-1/skasch.py` to test the submission.
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
        == 198
    )
