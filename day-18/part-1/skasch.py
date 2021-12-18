import dataclasses as dc
import heapq
import string
from typing import Iterable, List, Optional, Tuple

from tool.runners.python import SubmissionPy


@dc.dataclass
class Node:
    val: Optional[int] = None
    parent: Optional["Node"] = None
    left: Optional["Node"] = None  # type: ignore
    right: Optional["Node"] = None  # type: ignore

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
            node, _ = parse_line(stripped_line)
            assert isinstance(node, Node)
            yield node


DEPTH = 5


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
class LinkedListNode:
    node: Node
    index: int
    depth: int
    prv: Optional["LinkedListNode"] = None  # type: ignore
    nxt: Optional["LinkedListNode"] = None  # type: ignore

    def __repr__(self) -> str:
        s = f"{self.node}[{self.index}|{self.depth}]"
        if self.nxt is None:
            return s
        return f"{s}->{self.nxt}"

    def __lt__(self, other: "LinkedListNode") -> bool:
        return self.index < other.index


def add(left: Node, right: Node) -> Node:
    node = Node(left=left, right=right)
    left.parent = node
    right.parent = node
    head = None
    tail = head
    toodeep: List[LinkedListNode] = []
    toohigh: List[LinkedListNode] = []
    for leaf, depth, index in iterate_leaves(node):
        new_node = LinkedListNode(leaf, index, depth, prv=tail)
        if head is None or tail is None:
            head = new_node
            tail = new_node
        else:
            tail.nxt = new_node
            tail = tail.nxt
        if depth == DEPTH:
            heapq.heappush(toodeep, tail)
    while toodeep or toohigh:
        if toodeep:
            try:
                left_node = heapq.heappop(toodeep)
                left_leaf = left_node.node
                right_node = heapq.heappop(toodeep)
                right_leaf = right_node.node
            except AttributeError:
                continue
            assert left_leaf.val is not None
            assert right_leaf.val is not None
            prev_node = left_node.prv
            next_node = right_node.nxt
            if prev_node is not None:
                assert prev_node.node.val is not None
                prev_node.node.val += left_leaf.val
                if prev_node.node.val >= 10:
                    heapq.heappush(toohigh, prev_node)
            if next_node is not None:
                assert next_node.node.val is not None
                next_node.node.val += right_leaf.val
                if next_node.node.val >= 10:
                    heapq.heappush(toohigh, next_node)
            parent = left_leaf.parent
            assert parent is not None
            parent.left = None
            parent.right = None
            parent.val = 0
            new_node = LinkedListNode(parent, left_node.index, left_node.depth - 1)
            if prev_node is not None:
                prev_node.nxt = new_node
                new_node.prv = prev_node
            if next_node is not None:
                next_node.prv = new_node
                new_node.nxt = next_node
            del left_node.node
            del right_node.node
        elif toohigh:
            high_node = heapq.heappop(toohigh)
            try:
                leaf = high_node.node
            except AttributeError:
                continue
            if leaf.val is None:
                continue
            left_val = leaf.val // 2
            right_val = leaf.val - left_val
            left_leaf = Node(left_val, leaf)
            right_leaf = Node(right_val, leaf)
            leaf.val = None
            leaf.left = left_leaf
            leaf.right = right_leaf
            left_node = LinkedListNode(left_leaf, high_node.index, high_node.depth + 1)
            right_node = LinkedListNode(
                right_leaf,
                high_node.index + (1 << (DEPTH - high_node.depth - 1)),
                high_node.depth + 1,
                prv=left_node,
            )
            left_node.nxt = right_node
            if high_node.prv is not None:
                high_node.prv.nxt = left_node
                left_node.prv = high_node.prv
            if high_node.nxt is not None:
                high_node.nxt.prv = right_node
                right_node.nxt = high_node.nxt
            if high_node.depth + 1 >= DEPTH:
                heapq.heappush(toodeep, left_node)
                heapq.heappush(toodeep, right_node)
            else:
                if left_node.node.val is not None and left_node.node.val >= 10:
                    heapq.heappush(toohigh, left_node)
                if right_node.node.val is not None and right_node.node.val >= 10:
                    heapq.heappush(toohigh, right_node)
            del high_node.node
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
        number = None
        for num in parse(s):
            if number is None:
                number = num
            else:
                number = add(number, num)
        assert number is not None
        return magnitude(number)


def test_skasch() -> None:
    """
    Run `python -m pytest ./day-18/part-1/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
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
""".strip()
        )
        == 3488
    )
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
        == 4140
    )
