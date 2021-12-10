from tool.runners.python import SubmissionPy

from collections import deque


class DivSubmission(SubmissionPy):
    CHUNK_OPENERS = {"(": ")", "[": "]", "<": ">", "{": "}"}
    CHUNK_CLOSERS = {")": "(", "]": "[", ">": "<", "}": "{"}

    # ): 1 point.
    # ]: 2 points.
    # }: 3 points.
    # >: 4 points.
    POINTS_TABLE = {")": 1, "]": 2, "}": 3, ">": 4}

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        all_scores = []
        lines = s.split("\n")
        # all_scores = sorted([score for line in lines if (score := self.run_line(line)) is not None]) that would work only with python >= 3.8, so I'll avoid using to not break everyone's workflow
        all_scores = []
        for line in lines:
            score = self.run_line(line)
            if score is not None:
                all_scores.append(score)
        all_scores = sorted(all_scores)

        assert len(all_scores) % 2 == 1
        return sorted(all_scores)[(len(all_scores) >> 1)]

    def run_line(self, line):
        q = deque()
        is_corrupted = False
        for c in line:
            if c in self.CHUNK_CLOSERS:
                c2 = q.pop()
                if c2 != self.CHUNK_CLOSERS[c]:
                    is_corrupted = True
                    break

            else:
                q.append(c)

        if is_corrupted:
            return None

        points = 0
        while q:
            c = q.pop()
            points = points * 5 + self.POINTS_TABLE[self.CHUNK_OPENERS[c]]
        return points


def test_div():
    """
    Run `python -m pytest ./day-10/part-1/div.py` to test the submission.
    """
    assert (
        DivSubmission().run(
            """
""".strip()
        )
        == None
    )
