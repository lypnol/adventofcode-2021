from collections import Counter
from typing import Dict

from tool.runners.python import SubmissionPy

N_STEPS = 40


class ThomrenSubmission(SubmissionPy):
    def run(self, s, n_steps=N_STEPS):
        """
        :param s: input in string format
        :return: solution flag
        """
        polymer, rules_str = s.split("\n\n")

        self.rules = {}
        for line in rules_str.splitlines():
            fr, to = line.split(" -> ")
            self.rules[fr] = to

        self.memo = {}
        counts = Counter(list(polymer))
        for i in range(len(polymer) - 1):
            counts += self.grow(polymer[i : i + 2], n_steps)
        mc = counts.most_common()
        return int(mc[0][1]) - int(mc[-1][1])

    def grow(
        self,
        polymer: str,
        n: int,
    ):
        if (polymer, n) in self.memo:
            return self.memo[(polymer, n)]

        new = self.rules.get(polymer)
        if new is None or n == 0:
            return Counter()

        res = (
            self.grow(polymer[0] + new, n - 1)
            + self.grow(new + polymer[1], n - 1)
            + Counter([new])
        )
        self.memo[(polymer, n)] = res
        return res


def test_thomren():
    """
    Run `python -m pytest ./day-14/part-2/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
""".strip()
        )
        == 2188189693529
    )
