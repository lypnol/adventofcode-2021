from tool.runners.python import SubmissionPy

from itertools import permutations

digit_combinations = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        possible_combinations = set(digit_combinations.keys())
        score = 0

        for line in s.splitlines():
            # Simple brute-force solution
            for a, b, c, d, e, f, g in permutations('abcdefg'):
                is_valid = True
                mapping = {
                    "a": a,
                    "b": b,
                    "c": c,
                    "d": d,
                    "e": e,
                    "f": f,
                    "g": g,
                }
                combinations = line.replace(" | ", " ").split(" ")
                for combination in combinations:
                    mapped = "".join(sorted(mapping[l] for l in combination))
                    if mapped not in possible_combinations:
                        # invalid mapping
                        is_valid = False
                        break
                if is_valid:
                    break

            nb = []
            for combination in line.split(" | ")[1].split(" "):
                digit = digit_combinations["".join(
                    sorted([mapping[l] for l in combination]))]
                nb.append(str(digit))

            score += int("".join(nb))

        return score


def test_th_ch():
    """
    Run `python -m pytest ./day-08/part-1/th-ch.py` to test the submission.
    """
    assert (ThChSubmission().run("""
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
""".strip()) == 61229)
