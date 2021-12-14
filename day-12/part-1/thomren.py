from typing import Dict, List
from collections import defaultdict

from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        graph = parse_graph(s)
        return backtrack("start", graph, frozenset(["start"]))[1]


def backtrack(node, graph, visited):
    if node == "end":
        return (True, 1)

    res = (False, 0)
    for neighbor in graph[node]:
        if neighbor.islower() and neighbor in visited:
            continue
        found, n_paths = backtrack(neighbor, graph, visited | frozenset([neighbor]))
        res = (res[0] | found, res[1] + n_paths)

    return res


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
