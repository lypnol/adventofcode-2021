from tool.runners.python import SubmissionPy


def parse(s):
    depth = 0
    res = []  # List of []
    for char in s:
        if char == "[":
            depth += 1
            continue
        if char == "]":
            depth -= 1
            continue
        if char == ",":
            continue
        res.append([int(char), depth])

    return res


def explode(s):
    current_depth = -1
    has_exploded = False
    for i, (value, depth) in enumerate(s):
        if current_depth != depth:
            current_depth = depth
            continue

        # i = right, i-1 = left
        if depth > 4:
            if i - 2 >= 0:
                s[i - 2][0] += s[i - 1][0]
            if i + 1 < len(s):
                s[i + 1][0] += s[i][0]

            should_merge_to_left = i - 2 >= 0 and s[i - 2][1] == depth - 1
            if should_merge_to_left:
                s[i - 1] = [0, depth - 1]
                s.remove(s[i])
            else:
                s[i] = [0, depth - 1]
                s.remove(s[i - 1])

            has_exploded = True
            break
    return has_exploded


def split(s):
    has_split = False
    for i, (value, depth) in enumerate(s):
        if value >= 10:
            left = value // 2
            right = value - left
            s[i] = [right, depth + 1]
            s.insert(i, [left, depth + 1])
            has_split = True
            break
    return has_split


def reduce(s):
    while True:
        if explode(s):
            continue
        if split(s):
            continue
        break


def add(s1, s2):
    s = [[value, depth + 1] for value, depth in s1] + [[value, depth + 1]
                                                       for value, depth in s2]
    reduce(s)
    return s


def get_magnitude(s):
    if len(s) == 1:
        return s[0][0]

    # find the deepest node
    index = 0
    deepest = -1
    for i, (value, depth) in enumerate(s):
        if depth > deepest:
            deepest = depth
            index = i

    s[index] = [3 * s[index][0] + 2 * s[index + 1][0], deepest - 1]
    s.remove(s[index + 1])

    return get_magnitude(s)


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        nb = None
        for line in s.splitlines():
            if nb is None:
                nb = parse(line)
            else:
                nb = add(nb, parse(line))

        return get_magnitude(nb)


def test_th_ch():
    """
    Run `python -m pytest ./day-18/part-1/th-ch.py` to test the submission.
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
""".strip()) == 4140)
