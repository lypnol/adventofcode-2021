from tool.runners.python import SubmissionPy
from collections import defaultdict, deque


class SilvestreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        edges = defaultdict(set)
        for line in s.split("\n"):
            a, b = line.split("-")
            edges[a].add(b)
            edges[b].add(a)
        unfinished_paths = deque([("start", {"start", }, False)])
        counter = 0
        while unfinished_paths:
        #for _ in range(10):
            current, previous, twice_previous  = unfinished_paths.pop()
            for next in edges[current]:
                if next == "start":
                    continue
                if next == "end":
                    counter+=1
                else:
                    small_cave = next.upper() != next
                    if not ((small_cave and next in previous) and twice_previous):
                        unfinished_paths.append((next, previous | {next,}, twice_previous or (small_cave and next in previous)))
        return counter


def test_silvestre():
    """
    Run `python -m pytest ./day-12/part-1/silvestre.py` to test the submission.
    """
    assert (
        SilvestreSubmission().run(
            """
""".strip()
        )
        == None
    )
