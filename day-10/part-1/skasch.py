from typing import Iterable
from tool.runners.python import SubmissionPy


POINTS = {")": 3, "]": 57, "}": 1197, ">": 25137}
CLOSING = {"(": ")", "[": "]", "{": "}", "<": ">"}


def parse(s: str) -> Iterable[str]:
    for line in s.splitlines():
        if stripped_line := line.strip():
            yield stripped_line


class SkaschSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        res = 0
        for line in parse(s):
            stack = []
            for char in line:
                if char in CLOSING:
                    stack.append(char)
                    continue
                left = stack.pop()
                if CLOSING[left] != char:
                    res += POINTS[char]
                    break
        return res


def test_skasch():
    """
    Run `python -m pytest ./day-10/part-1/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""".strip()
        )
        == 26397
    )
