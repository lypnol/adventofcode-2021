from typing import SupportsComplex
from tool.runners.python import SubmissionPy

from collections import deque


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        score = 0
        for line in s.splitlines():
            chunks = deque()
            for character in line:
                if character == "(":
                    chunks.appendleft(")")
                elif character == "[":
                    chunks.appendleft("]")
                elif character == "{":
                    chunks.appendleft("}")
                elif character == "<":
                    chunks.appendleft(">")
                else:
                    expected = chunks.popleft()
                    if character != expected:
                        # invalid chunk
                        if character == ")":
                            score += 3
                        elif character == "]":
                            score += 57
                        elif character == "}":
                            score += 1197
                        elif character == ">":
                            score += 25137

        return score


def test_th_ch():
    """
    Run `python -m pytest ./day-10/part-1/th-ch.py` to test the submission.
    """
    assert (ThChSubmission().run("""
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
""".strip()) == 26397)
