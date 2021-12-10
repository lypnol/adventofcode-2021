from tool.runners.python import SubmissionPy

from collections import deque


class DivSubmission(SubmissionPy):
    CHUNK_CLOSERS = {")": "(", "]": "[", ">": "<", "}": "{"}

    # ): 3 points.
    # ]: 57 points.
    # }: 1197 points.
    # >: 25137 points.
    POINTS_TABLE = {")": 3, "]": 57, "}": 1197, ">": 25137}

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        points = 0
        for line in s.split("\n"):
            q = deque()
            for c in line:
                if c in self.CHUNK_CLOSERS:
                    c2 = q.pop()
                    if c2 != self.CHUNK_CLOSERS[c]:
                        points += self.POINTS_TABLE[c]
                        break

                else:
                    q.append(c)
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
