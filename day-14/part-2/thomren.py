from collections import Counter
from functools import lru_cache
from typing import Dict, Counter as CounterType

from tool.runners.python import SubmissionPy

N_STEPS = 40


class ThomrenSubmission(SubmissionPy):
    def run(self, s, n_steps=N_STEPS):
        """
        :param s: input in string format
        :return: solution flag
        """
        polymer, rules_str = s.split("\n\n")

        rules = {}
        for line in rules_str.splitlines():
            fr, to = line.split(" -> ")
            rules[fr] = to

        counts = count_polymers(polymer, rules, n_steps)

        mc = counts.most_common()
        return int(mc[0][1]) - int(mc[-1][1])


def count_polymers(start: str, rules: Dict[str, str], n_steps: int) -> CounterType[str]:
    @lru_cache(None)
    def grow(
        polymer: str,
        n: int,
    ) -> CounterType[str]:
        new = rules.get(polymer)
        if new is None or n == 0:
            return Counter()

        return (
            grow(polymer[0] + new, n - 1)
            + grow(new + polymer[1], n - 1)
            + Counter([new])
        )

    return sum(
        (grow(start[i : i + 2], n_steps) for i in range(len(start) - 1)),
        Counter(list(start)),
    )


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
