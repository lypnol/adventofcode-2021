from functools import reduce
import json

from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        snailfish_numbers = [json.loads(line) for line in s.splitlines()]
        return magnitude(add_numbers(snailfish_numbers))


def add_numbers(snailfish_numbers):
    return reduce(lambda x, y: add(x, y), snailfish_numbers)


def add(snailfish_n1, snailfish_n2):
    return snailfish_reduce([snailfish_n1, snailfish_n2])


def snailfish_reduce(snailfish_n):
    finished = False
    while not finished:
        has_exploded, _, _, snailfish_n = explode(snailfish_n)
        finished = not has_exploded

        if not has_exploded:
            has_split, snailfish_n = split(snailfish_n)
            finished = not has_split

    return snailfish_n


def explode(snailfish_n, max_depth=4):
    if type(snailfish_n) == int:
        return (False, None, None, snailfish_n)

    if max_depth == 0:
        return (True, snailfish_n[0], snailfish_n[1], 0)

    e, l, r, sn = explode(snailfish_n[0], max_depth=max_depth - 1)
    if e:
        right = add_leftmost(snailfish_n[1], r) if r is not None else snailfish_n[1]
        return (
            True,
            l,
            None,
            [sn, right],
        )

    e, l, r, sn = explode(snailfish_n[1], max_depth=max_depth - 1)
    if e:
        left = add_rightmost(snailfish_n[0], l) if l is not None else snailfish_n[0]
        return (True, None, r, [left, sn])

    return False, None, None, snailfish_n


def add_leftmost(snailfish_number, n):
    if type(snailfish_number) == int:
        return snailfish_number + n
    else:
        return [add_leftmost(snailfish_number[0], n), snailfish_number[1]]


def add_rightmost(snailfish_number, n):
    if type(snailfish_number) == int:
        return snailfish_number + n
    else:
        return [snailfish_number[0], add_rightmost(snailfish_number[1], n)]


def split(snailfish_n):
    if type(snailfish_n) == int:
        if snailfish_n >= 10:
            half = snailfish_n // 2
            return (
                True,
                [
                    half,
                    snailfish_n - half,
                ],
            )
        else:
            return (False, snailfish_n)
    else:
        has_splitted, left = split(snailfish_n[0])
        if has_splitted:
            return (True, [left, snailfish_n[1]])

        has_splitted, right = split(snailfish_n[1])
        if has_splitted:
            return (True, [snailfish_n[0], right])

        return (False, snailfish_n)


def magnitude(snailfish_n):
    if type(snailfish_n) == int:
        return snailfish_n

    return 3 * magnitude(snailfish_n[0]) + 2 * magnitude(snailfish_n[-1])


def test_thomren():
    """
    Run `python -m pytest ./day-18/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
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
""".strip()
        )
        == 4140
    )


def test_magnitude():
    assert magnitude([[1, 2], [[3, 4], 5]]) == 143
    assert magnitude([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]) == 1384
    assert magnitude([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]) == 445
    assert magnitude([[[[3, 0], [5, 3]], [4, 4]], [5, 5]]) == 791
    assert magnitude([[[[5, 0], [7, 4]], [5, 5]], [6, 6]]) == 1137
    assert (
        magnitude([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]])
        == 3488
    )


def test_explode():
    for sn, expected in [
        ([[[[[9, 8], 1], 2], 3], 4], [[[[0, 9], 2], 3], 4]),
        ([7, [6, [5, [4, [3, 2]]]]], [7, [6, [5, [7, 0]]]]),
        ([[6, [5, [4, [3, 2]]]], 1], [[6, [5, [7, 0]]], 3]),
        (
            [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]],
            [[3, [2, [8, 0]]], [9, [5, [7, 0]]]],
        ),
    ]:

        assert explode(sn)[-1] == expected


def test_reduce():
    sn = [[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]
    assert snailfish_reduce(sn) == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]


def test_add_numbers():
    for s, expected in [
        (
            """
[1,1]
[2,2]
[3,3]
[4,4]
""",
            [[[[1, 1], [2, 2]], [3, 3]], [4, 4]],
        ),
        (
            """
[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
""",
            [[[[3, 0], [5, 3]], [4, 4]], [5, 5]],
        ),
        (
            """
[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]
""",
            [[[[5, 0], [7, 4]], [5, 5]], [6, 6]],
        ),
        (
            """
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
""",
            [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]],
        ),
        (
            """
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
""",
            [
                [[[6, 6], [7, 6]], [[7, 7], [7, 0]]],
                [[[7, 7], [7, 7]], [[7, 8], [9, 9]]],
            ],
        ),
    ]:
        snailfish_numbers = [json.loads(line) for line in s.strip().splitlines()]
        assert add_numbers(snailfish_numbers) == expected
