from typing import Dict, List
from collections import defaultdict
from functools import lru_cache

from tool.runners.python import SubmissionPy

START = "start"
END = "end"


class ThomrenSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        graph = parse_graph(s)
        return count_paths(graph, START, END)


def count_paths(graph, start, target):
    @lru_cache
    def backtrack(node, visited):
        if node == target:
            return (True, 1)
        visited = visited | frozenset([node])

        res = (False, 0)
        for neighbor in graph[node]:
            if neighbor.islower() and neighbor in visited:
                continue
            found, n_paths = backtrack(neighbor, visited)
            res = (res[0] | found, res[1] + n_paths)

        return res

    return backtrack(start, frozenset())[1]


def parse_graph(s: str) -> Dict[str, List[str]]:
    graph = defaultdict(list)
    for line in s.splitlines():
        src, dest = line.split("-")
        graph[src].append(dest)
        graph[dest].append(src)
    return graph


def test_thomren():
    """
    Run `python -m pytest ./day-12/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""".strip()
        )
        == 10
    )

    assert (
        ThomrenSubmission().run(
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
""".strip()
        )
        == 19
    )

    assert (
        ThomrenSubmission().run(
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
start-RW""".strip()
        )
        == 226
    )
