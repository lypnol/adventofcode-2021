import dataclasses as dc
import heapq
import itertools
import string
from typing import Iterable, List, Optional, Tuple

from tool.runners.python import SubmissionPy


@dc.dataclass
class Node:
    val: Optional[int] = None
    parent: Optional["Node"] = None
    left: Optional["Node"] = None  # type: ignore
    right: Optional["Node"] = None  # type: ignore

    def copy(self) -> "Node":
        if self.val is not None:
            return Node(self.val)
        res = Node()
        if self.left is not None:
            left = self.left.copy()
            res.left = left
            left.parent = res
        if self.right is not None:
            right = self.right.copy()
            res.right = right
            right.parent = res
        return res

    def __repr__(self) -> str:
        if self.val is not None:
            return str(self.val)
        return f"[{self.left},{self.right}]"


DIGITS = set(string.digits)


def parse_line(line: str, idx: int = 0) -> Tuple[Node, int]:
    if line[idx] in DIGITS:
        return Node(val=int(line[idx])), idx + 1
    if line[idx] == "[":
        left, idx = parse_line(line, idx + 1)
        assert line[idx] == ","
        right, idx = parse_line(line, idx + 1)
        assert line[idx] == "]"
        res = Node(left=left, right=right)
        left.parent = res
        right.parent = res
        return res, idx + 1
    raise ValueError


def parse(s: str) -> Iterable[Node]:
    for line in s.splitlines():
        if stripped_line := line.strip():
            yield parse_line(stripped_line)[0]


DEPTH = 5
N = 1 << DEPTH


def iterate_leaves(
    root: Node, depth: int = 0, path: int = 0
) -> Iterable[Tuple[Node, int, int]]:
    if root.val is not None:
        yield root, depth, path << (DEPTH - depth)
        return
    if root.left is not None:
        yield from iterate_leaves(root.left, depth + 1, path << 1)
    if root.right is not None:
        yield from iterate_leaves(root.right, depth + 1, (path << 1) + 1)


@dc.dataclass
class Bundle:
    node: Node
    index: int
    depth: int

    def __lt__(self, other: "Bundle") -> bool:
        return self.index < other.index


def process_toodeep(
    left_bundle: Bundle,
    right_bundle: Bundle,
    toohigh: List[int],
    bundles: List[Optional[Bundle]],
) -> None:
    left_leaf = left_bundle.node
    right_leaf = right_bundle.node
    assert left_leaf.val is not None and right_leaf.val is not None
    prev_bundle = None
    for prev_index in reversed(range(left_bundle.index)):
        prev_bundle = bundles[prev_index]
        if prev_bundle is not None:
            break
    next_bundle = None
    for next_index in range(right_bundle.index + 1, N):
        next_bundle = bundles[next_index]
        if next_bundle is not None:
            break
    parent = left_leaf.parent
    assert parent is not None
    parent.left = None
    parent.right = None
    parent.val = 0
    bundles[right_bundle.index] = None
    new_bundle = Bundle(parent, left_bundle.index, left_bundle.depth - 1)
    bundles[left_bundle.index] = new_bundle
    if prev_bundle is not None:
        assert prev_bundle.node.val is not None
        prev_bundle.node.val += left_leaf.val
        if prev_bundle.node.val >= 10:
            heapq.heappush(toohigh, prev_bundle.index)
    if next_bundle is not None:
        assert next_bundle.node.val is not None
        next_bundle.node.val += right_leaf.val
        if next_bundle.node.val >= 10:
            heapq.heappush(toohigh, next_bundle.index)


def process_toohigh(
    toohigh: List[int], toodeep: List[int], bundles: List[Optional[Bundle]]
) -> None:
    high_bundle = bundles[heapq.heappop(toohigh)]
    assert high_bundle is not None
    leaf = high_bundle.node
    if leaf.val is None:
        return
    if leaf.val < 10:
        return
    left_val = leaf.val // 2
    right_val = leaf.val - left_val
    left_leaf = Node(left_val, leaf)
    right_leaf = Node(right_val, leaf)
    leaf.val = None
    leaf.left = left_leaf
    leaf.right = right_leaf
    left_bundle = Bundle(left_leaf, high_bundle.index, high_bundle.depth + 1)
    right_index = high_bundle.index + (1 << (DEPTH - high_bundle.depth - 1))
    right_bundle = Bundle(
        right_leaf,
        right_index,
        high_bundle.depth + 1,
    )
    bundles[high_bundle.index] = left_bundle
    bundles[right_index] = right_bundle
    if high_bundle.depth + 1 >= DEPTH:
        heapq.heappush(toodeep, left_bundle.index)
        heapq.heappush(toodeep, right_bundle.index)
    else:
        if left_bundle.node.val is not None and left_bundle.node.val >= 10:
            heapq.heappush(toohigh, left_bundle.index)
        if right_bundle.node.val is not None and right_bundle.node.val >= 10:
            heapq.heappush(toohigh, right_bundle.index)


def add(left: Node, right: Node) -> Node:
    node = Node(left=left, right=right)
    left.parent = node
    right.parent = node
    bundles: List[Optional[Bundle]] = [None] * N
    toodeep: List[int] = []
    toohigh: List[int] = []
    for leaf, depth, index in iterate_leaves(node):
        bundle = Bundle(leaf, index, depth)
        bundles[index] = bundle
        if depth == DEPTH:
            heapq.heappush(toodeep, index)
    while toodeep or toohigh:
        if toodeep:
            left_bundle = bundles[heapq.heappop(toodeep)]
            right_bundle = bundles[heapq.heappop(toodeep)]
            assert left_bundle is not None
            assert right_bundle is not None
            process_toodeep(left_bundle, right_bundle, toohigh, bundles)
        elif toohigh:
            process_toohigh(toohigh, toodeep, bundles)
    return node


def magnitude(root: Node) -> int:
    if root.val is not None:
        return root.val
    res = 0
    if root.left is not None:
        res += 3 * magnitude(root.left)
    if root.right is not None:
        res += 2 * magnitude(root.right)
    return res


class SkaschSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        return max(
            magnitude(add(num1.copy(), num2.copy()))
            for num1, num2 in itertools.permutations(parse(s), 2)
        )


def test_skasch() -> None:
    """
    Run `python -m pytest ./day-18/part-2/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
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
        == 3993
    )
