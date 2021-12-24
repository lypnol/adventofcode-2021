from importlib import import_module
from itertools import permutations

from tool.runners.python import SubmissionPy

part1 = import_module("day-18.part-1.th-ch")


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        nbs = [part1.parse(line) for line in s.splitlines()]
        max_magnitude = -1
        for x, y in permutations(nbs, 2):
            max_magnitude = max(max_magnitude,
                                part1.get_magnitude(part1.add(x, y)))
            max_magnitude = max(max_magnitude,
                                part1.get_magnitude(part1.add(y, x)))
        return max_magnitude


def test_th_ch():
    """
    Run `python -m pytest ./day-18/part-2/th-ch.py` to test the submission.
    """
    assert (ThChSubmission().run("""
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""".strip()) == 3993)
