from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):
    def run(self, s):
        to_closings = {
            "(": ")",
            "[": "]",
            "{": "}",
            "<": ">",
        }
        points = {
            ")": 3,
            "]": 57,
            "}": 1197,
            ">": 25137,
        }

        score = 0
        for l in s.splitlines():
            stack = []
            for c in l:
                if c in to_closings:
                    stack.append(c)
                else:
                    expected = to_closings[stack.pop()]
                    if c != expected:
                        score += points[c]
                        break

        return score


def test_jon():
    """
    Run `python -m pytest ./day-10/part-1/jon.py` to test the submission.
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
        == 26397
    )
