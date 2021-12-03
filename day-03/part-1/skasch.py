import collections
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
        counter = collections.Counter()
        n_lines = 0
        n_chars = None
        for line in self.parse(s):
            n_lines += 1
            if n_chars is None:
                n_chars = len(line)
            for idx, char in enumerate(line):
                if char == "1":
                    counter[n_chars - 1 - idx] += 1
        gamma = sum(1 << n for n, count in counter.items() if 2 * count > n_lines)
        epsilon = gamma ^ ((1 << n_chars) - 1)
        print(gamma, epsilon)
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
