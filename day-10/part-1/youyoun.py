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
        open_chars = {'<', '{', '[', '('}
        close_chars = {'>': 25137, '}': 1197, ')': 3, ']': 57}
        counter = 0
        for l in s.splitlines():
            open_stack = []
            for c in l:
                if c in open_chars:
                    open_stack.append(c)
                elif c in close_chars:
                    if not is_char_close(open_stack.pop(), c):
                        counter += close_chars[c]
                        break
        return counter


def test_youyoun():
    """
    Run `python -m pytest ./day-10/part-1/youyoun.py` to test the submission.
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
            == 26397
    )
