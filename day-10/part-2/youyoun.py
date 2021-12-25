from tool.runners.python import SubmissionPy


def is_char_close(open_char, close_char):
    if open_char == '<' and close_char == '>' or open_char == '[' and close_char == ']' or open_char == '{' and close_char == '}' or open_char == '(' and close_char == ')':
        return True
    return False


class YouyounSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        open_chars = {'<': '>', '{': '}', '[': ']', '(': ')'}
        close_chars = {'>': 4, '}': 3, ')': 1, ']': 2}
        scores = []
        for l in s.splitlines():
            open_stack = []
            is_broken = False
            for c in l:
                if c in open_chars:
                    open_stack.append(c)
                elif c in close_chars:
                    if not is_char_close(open_stack.pop(), c):
                        is_broken = True
                        break
            if is_broken:
                continue
            total_score = 0
            for i in range(len(open_stack) - 1, -1, -1):
                total_score = total_score * 5 + close_chars[open_chars[open_stack[i]]]
            scores.append(total_score)
        return sorted(scores)[len(scores) // 2]


def test_youyoun():
    """
    Run `python -m pytest ./day-10/part-2/youyoun.py` to test the submission.
    """
    assert (
            YouyounSubmission().run(
                """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]""".strip()
            )
            == 288957
    )
