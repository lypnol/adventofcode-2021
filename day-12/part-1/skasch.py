import collections
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
    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        graph = parse(s)
        small_caves = {cave for cave in graph if cave == cave.lower()}
        # State: (position, visited)
        stack = [(START, {START})]
        res = 0
        while stack:
            (
                position,
                visited,
            ) = stack.pop()
            for next_pos in graph[position]:
                if next_pos in visited:
                    continue
                if next_pos == END:
                    res += 1
                    continue
                next_visited = {next_pos} if next_pos in small_caves else set()
                stack.append((next_pos, visited | next_visited))
        return res


def test_skasch():
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
