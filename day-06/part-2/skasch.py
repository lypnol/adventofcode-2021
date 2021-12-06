
import collections
from typing import List
from tool.runners.python import SubmissionPy


DAYS = 256
CYCLE = 7
NEW = 2


def parse(s: str) -> List[str]:
    return s.split(",")


class SkaschSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        cnt = collections.Counter([int(v) for v in parse(s)])
        d = DAYS
        while d >= CYCLE:
            tmp_cnt = collections.Counter()
            for v in range(CYCLE, CYCLE + NEW):
                tmp_cnt[v - CYCLE] += cnt[v]
                del cnt[v]
            cnt += collections.Counter({v + 2: n for v, n in cnt.items()})
            cnt += tmp_cnt
            d -= CYCLE
        return sum(n * (1 if v >= d else 2) for v, n in cnt.items())


def test_skasch():
    """
    Run `python -m pytest ./day-06/part-1/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
3,4,3,1,2
""".strip()
        )
        == 26984457539
    )
