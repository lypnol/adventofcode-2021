from tool.runners.python import SubmissionPy

from typing import *
from collections import deque

class Leaf:
    def __init__(self, value: int) -> None:
        self.parent = None
        self.next = None
        self.previous = None
        self.value = value

    def set_next(self, next: 'Leaf') -> None:
        self.next = next
        next.previous = self

    def __str__(self) -> str:
        return str(self.value)

    def magnitude(self) -> int:
        return self.value

class Tree:
    @classmethod
    def add(cls, left: 'Tree', right: 'Tree') -> 'Tree':
        root = Tree(left, right)
        left.rightmost_leaf().set_next(right.leftmost_leaf())
        return root

    def __init__(self, left: Union['Tree', 'Leaf'], right: Union['Tree', 'Leaf']) -> None:
        self.parent = None
        self.left = left
        self.right = right

        self.left.parent = self
        self.right.parent = self

    def __str__(self) -> str:
        return f"[{str(self.left)},{str(self.right)}]"

    def magnitude(self) -> int:
        return 3*self.left.magnitude() + 2*self.right.magnitude()

    def leftmost_leaf(self):
        node = self
        while not isinstance(node, Leaf):
            node = node.left
        return node

    def rightmost_leaf(self):
        node = self
        while not isinstance(node, Leaf):
            node = node.right
        return node

    def replace_child(self, old_child, new_child):
        if self.left == old_child:
            self.left = new_child
        elif self.right == old_child:
            self.right = new_child
        else:
            raise Exception("uh oh")

class DivSubmission(SubmissionPy):
    def find_pair_to_explode(self, root: Tree) -> Optional[Tree]:
        q = deque([(0, root)])
        while q:
            depth, node = q.pop()
            if depth == 4:
                return node

            if isinstance(node.right, Tree):
                q.append((depth+1, node.right))
            if isinstance(node.left, Tree):
                q.append((depth+1, node.left))

        return None

    def explode(self, root: Tree) -> bool:
        # find the first pair to explode if it exists:
        pair = self.find_pair_to_explode(root)
        if pair is None:
            return False

        leaf = Leaf(0)
        leaf.parent = pair.parent

        previous: Optional[Leaf] = pair.left.previous
        if previous is not None:
            previous.value += pair.left.value
            previous.set_next(leaf)
        next: Optional[Leaf] = pair.right.next
        if next is not None:
            next.value += pair.right.value
            leaf.set_next(next)

        pair.parent.replace_child(pair, leaf)

        return True

    def find_node_to_split(self, root: Tree):
        q = deque()
        q.append(root)
        while q:
            node = q.pop()
            if isinstance(node, Leaf):
                if node.value >= 10:
                    return node
                continue

            q.append(node.right)
            q.append(node.left)
        return None

    def split(self, root: Tree) -> bool:
        leaf = self.find_node_to_split(root)
        if leaf is None:
            return False

        left = Leaf(leaf.value >> 1)
        right = Leaf(leaf.value >> 1)
        if leaf.value % 2 == 1:
            right.value += 1

        left.previous = leaf.previous
        left.next = right
        right.next = leaf.next
        right.previous = left
        if leaf.previous is not None:
            leaf.previous.next = left
        if leaf.next is not None:
            leaf.next.previous = right

        tree = Tree(left, right)
        leaf.parent.replace_child(leaf, tree)
        tree.parent = leaf.parent
        return True

    def read_line(self, line):
        stack = deque()
        previous_leaf: Optional[Leaf] = None
        for c in line:
            if c.isdigit():
                leaf = Leaf(int(c))
                if previous_leaf is not None:
                    previous_leaf.set_next(leaf)
                previous_leaf = leaf
                stack.append(leaf)
            elif c == "]":
                right = stack.pop()
                left = stack.pop()
                tree = Tree(left, right)
                stack.append(tree)
        return stack.pop()

    def reduce_node(self, node: Tree):
        while True:
            if self.explode(node):
                continue

            if self.split(node):
                continue

            return node

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        lines = s.split("\n")
        n = len(lines)
        result = 0
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                left = self.read_line(lines[i])
                right = self.read_line(lines[j])
                node = Tree.add(left, right)
                node = self.reduce_node(node)
                magnitude = node.magnitude()
                if magnitude > result:
                    result = magnitude

        return result

def test_div():
    """
    Run `python -m pytest ./day-18/part-1/div.py` to test the submission.
    """
    assert (
        DivSubmission().run(
            """
""".strip()
        )
        == None
    )
