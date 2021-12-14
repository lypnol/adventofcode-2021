import collections
import functools
from typing import Dict, List, Tuple, Counter
from tool.runners.python import SubmissionPy


def parse(s: str) -> Tuple[List[str], Dict[Tuple[str, str], str]]:
    lines = s.splitlines()
    initial = list(lines[0].strip())
    mapping = {}
    for line in lines[2:]:
        if stripped_line := line.strip():
            left, right = stripped_line.split(" -> ", 1)
            mapping[left[0], left[1]] = right
    return initial, mapping


DEPTH = 40


class SkaschSubmission(SubmissionPy):
    @functools.lru_cache(None)
    def dfs(self, left: str, right: str, depth: int) -> Counter[str]:
        if depth == DEPTH:
            return collections.Counter()
        mid = self.mapping[left, right]
        cnt = collections.Counter(mid)
        return cnt + self.dfs(left, mid, depth + 1) + self.dfs(mid, right, depth + 1)

    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        self.dfs.cache_clear()
        initial, self.mapping = parse(s)
        cnt = collections.Counter(initial)
        for left, right in zip(initial, initial[1:]):
            cnt += self.dfs(left, right, 0)
        return max(cnt.values()) - min(cnt.values())


def test_skasch() -> None:
    """
    Run `python -m pytest ./day-14/part-2/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
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
