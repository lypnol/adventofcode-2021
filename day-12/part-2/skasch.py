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
        # State: (position, visited, visited_twice)
        # visited_twice is True if one small case has already been visited twice
        stack = [(START, set(), False)]
        res = 0
        while stack:
            (
                position,
                visited,
                visited_twice,
            ) = stack.pop()
            for next_pos in graph[position]:
                if visited_twice and next_pos in visited or next_pos == START:
                    continue
                if next_pos == END:
                    res += 1
                    continue
                next_visited = {next_pos} if next_pos in small_caves else set()
                stack.append((next_pos, visited | next_visited, visited_twice or next_pos in visited))
        return res


def test_skasch():
    """
    Run `python -m pytest ./day-12/part-2/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
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
        == 36
    )
