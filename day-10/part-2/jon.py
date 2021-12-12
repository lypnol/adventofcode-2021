from tool.runners.python import SubmissionPy
from statistics import median


class JonSubmission(SubmissionPy):
    def run(self, s):
        scores = [line_score(l) for l in s.splitlines()]
        return int(median(s for s in scores if s is not None))


to_closings = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

points = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}


def line_score(l):
    stack = []
    for c in l:
        if c in to_closings:
            stack.append(c)
        else:
            expected = to_closings[stack.pop()]
            if c != expected:
                return None  # Corrupted
    stack.reverse()
    score = 0
    for c in stack:
        score = score * 5 + points[c]
    return score


def test_jon():
    """
    Run `python -m pytest ./day-10/part-2/jon.py` to test the submission.
    """
    assert (
        JonSubmission().run(
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
        == 288957
    )
