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
        unfinished_paths = deque([("start", {"start",}),])
        counter = 0
        while unfinished_paths:
            current, previous = unfinished_paths.pop()
            for next in edges[current]:
                if next == "end":
                    counter+=1
                elif next.lower() != next or next not in previous:
                    unfinished_paths.append((next, previous | {next,}))
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
