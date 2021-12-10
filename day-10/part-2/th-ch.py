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
        scores = []
        for line in s.splitlines():
            chunks = deque()
            score = 0
            is_corrupted = False
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
                        is_corrupted = True
                        break

            if is_corrupted:
                continue
            if not chunks:
                # complete line
                continue

            for character in chunks:
                score *= 5
                if character == ")":
                    score += 1
                elif character == "]":
                    score += 2
                elif character == "}":
                    score += 3
                elif character == ">":
                    score += 4

            scores.append(score)

        return sorted(scores)[len(scores) // 2]


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
""".strip()) == 288957)
