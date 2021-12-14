import collections
import functools
from typing import DefaultDict, Set

from tool.runners.python import SubmissionPy


def parse(s: str) -> DefaultDict[str, Set[str]]:
    graph = collections.defaultdict(set)
    for line in s.splitlines():
        if stripped_line := line.strip():
            left, right = stripped_line.split("-")
            graph[left].add(right)
            graph[right].add(left)
    return graph


START = "start"
END = "end"


class SkaschSubmission(SubmissionPy):
    @functools.lru_cache(None)
    def dfs(self, position: str, visited: int) -> int:
        res = 0
        for next_pos in self.graph[position]:
            bpos = self.bits[next_pos]
            if bpos & visited:
                continue
            if next_pos == END:
                res += 1
                continue
            next_visited = visited
            if bpos & self.small_caves:
                next_visited |= bpos
            res += self.dfs(next_pos, next_visited)
        return res

    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        self.graph = parse(s)
        self.bits = {cave: 1 << idx for idx, cave in enumerate(self.graph)}
        self.small_caves = sum(self.bits[cave] for cave in self.graph if cave == cave.lower())
        self.dfs.cache_clear()
        return self.dfs(START, self.bits[START])


def test_skasch() -> None:
    """
    Run `python -m pytest ./day-12/part-1/skasch.py` to test the submission.
    """
    for input, output in [
        (
            """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""".strip(),
            10,
        ),
        (
            """
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
""".strip(),
            19,
        ),
        (
            """
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
""",
            226,
        ),
    ]:
        assert SkaschSubmission().run(input) == output
