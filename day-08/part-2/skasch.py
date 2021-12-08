from typing import Dict, Iterable, List, Tuple
import functools
from tool.runners.python import SubmissionPy


def parse(s: str) -> Iterable[Tuple[List[str], List[str]]]:
    for line in s.splitlines():
        if stripped_line := line.strip():
            all_digits, output = stripped_line.split(" | ", 1)
            yield all_digits.split(), output.split()


DIGITS = {
    "abcefg": "0",
    "cf": "1",
    "acdeg": "2",
    "acdfg": "3",
    "bcdf": "4",
    "abdfg": "5",
    "abdefg": "6",
    "acf": "7",
    "abcdefg": "8",
    "abcdfg": "9",
}


def get_digit(s: str, configuration: Dict[str, str]) -> str:
    real_s = "".join(sorted(configuration[c] for c in s))
    return DIGITS[real_s]


def process(all_digits: List[str]) -> Dict[str, str]:
    one = None
    four = None
    seven = None
    fivers = []
    sixers = []
    for value in all_digits:
        if len(value) == 2:
            one = set(value)
        elif len(value) == 3:
            seven = set(value)
        elif len(value) == 4:
            four = set(value)
        elif len(value) == 5:
            fivers.append(set(value))
        elif len(value) == 6:
            sixers.append(set(value))
    configuration = {}
    a = next(iter(seven - one))
    configuration[a] = "a"
    b_d = four - one
    a_d_g = functools.reduce(lambda l, r: l & r, fivers)
    d = next(iter(b_d & a_d_g))
    configuration[d] = "d"
    b = next(iter(b_d - {d}))
    configuration[b] = "b"
    g = next(iter(a_d_g - {a, d}))
    configuration[g] = "g"
    for fiver in fivers:
        if len(fiver - {a, b, d, g}) == 1:
            five = fiver
            break
    f = next(iter(fiver - {a, b, d, g}))
    configuration[f] = "f"
    for fiver in fivers:
        if fiver == five:
            continue
        if f in fiver:
            three = fiver
            break
    c = next(iter(three - {a, d, f, g}))
    configuration[c] = "c"
    e = next(iter(set("abcdefg") - {a, b, c, d, f, g}))
    configuration[e] = "e"
    return configuration


class SkaschSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        res = 0
        for all_digits, output in parse(s):
            configuration = process(all_digits)
            digits = [get_digit(d, configuration) for d in output]
            res += int("".join(digits))
        return res

def test_skasch():
    """
    Run `python -m pytest ./day-08/part-2/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""".strip()
        )
        == 61229
    )
