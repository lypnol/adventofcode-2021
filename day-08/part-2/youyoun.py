from tool.runners.python import SubmissionPy
from collections import Counter


def sort_str(str_):
    return "".join(sorted(str_))


class YouyounSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        digits = [[0, 1, 2, 4, 5, 6], [2, 5], [0, 2, 3, 4, 6], [0, 2, 3, 5, 6], [1, 2, 3, 5], [0, 1, 3, 5, 6],
                  [0, 1, 3, 4, 5, 6], [0, 2, 5], [0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 5, 6]]
        counter = 0
        for patterns in s.splitlines():
            deduce_segs, interest = patterns.split(" | ")
            chars = deduce_segs.split(" ")
            chars = list(map(sort_str, chars))
            pos = [-1 for _ in range(7)]
            number_segments = [None for _ in range(10)]
            c_counts = [[chr(97 + i), 0] for i in range(7)]
            for c in chars:
                if len(c) == 2:
                    number_segments[1] = c
                elif len(c) == 3:
                    number_segments[7] = c
                elif len(c) == 4:
                    number_segments[4] = c
                elif len(c) == 7:
                    number_segments[8] = c
                for e in c:
                    c_counts[ord(e) - 97][1] += 1
            c_counts = sorted(c_counts, key=lambda x: x[1])

            pos[0] = (set(number_segments[7]) - set(number_segments[1])).pop()
            for c, count in c_counts:
                if count == 9:
                    pos[5] = c
                elif count == 6:
                    pos[1] = c
                elif count == 4:
                    pos[4] = c
                    pos[6] = (set(number_segments[8]) - set(number_segments[4]) - {pos[0], pos[4]}).pop()
                elif count == 8 and c != pos[0]:
                    pos[2] = c
                elif count == 7 and c != pos[6]:
                    pos[3] = c
            digits_segs = {"".join(sorted([pos[i] for i in x])): i for i, x in enumerate(digits)}
            for i, segment in enumerate(map(sort_str, interest.split(" "))):
                counter += digits_segs[segment] * 10 ** (3 - i)
        return counter


def test_youyoun():
    """
    Run `python -m pytest ./day-08/part-2/youyoun.py` to test the submission.
    """
    assert (
            YouyounSubmission().run(
                """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce""".strip()
            )
            == 61229
    )
