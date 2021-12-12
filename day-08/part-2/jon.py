from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):
    def run(self, s):
        res = 0
        for l in s.splitlines():
            words = l.split(" ")
            m = mapping(words[:10])
            res += m[norm(words[11])] * 1000
            res += m[norm(words[12])] * 100
            res += m[norm(words[13])] * 10
            res += m[norm(words[14])] * 1

        return res


def mapping(words):
    words = [norm(w) for w in words]
    d = {}
    d[1] = next(w for w in words if len(w) == 2)
    d[4] = next(w for w in words if len(w) == 4)
    d[7] = next(w for w in words if len(w) == 3)
    d[8] = next(w for w in words if len(w) == 7)

    set069 = {w for w in words if len(w) == 6}
    d[9] = next(w for w in set069 if all(l in w for l in d[4]))
    set06 = set069 - {d[9]}
    d[0] = next(w for w in set06 if all(l in w for l in d[1]))
    d[6] = next(iter(set06 - {d[0]}))

    set235 = {w for w in words if len(w) == 5}
    d[3] = next(w for w in set235 if all(l in w for l in d[1]))
    d[2] = next(w for w in set235 if sum(1 for l in d[4] if l in w) == 2)
    d[5] = next(iter(set235 - {d[3], d[2]}))

    return {v: k for k, v in d.items()}


def norm(w):
    return "".join(sorted(w))


def test_jon():
    """
    Run `python -m pytest ./day-08/part-2/jon.py` to test the submission.
    """
    assert (
        JonSubmission().run(
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
