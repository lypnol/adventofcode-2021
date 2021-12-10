from typing import Iterable, List, Optional, Tuple
from tool.runners.python import SubmissionPy


POINTS = {")": 1, "]": 2, "}": 3, ">": 4}
CLOSING = {"(": ")", "[": "]", "{": "}", "<": ">"}


def parse(s: str) -> Iterable[str]:
    for line in s.splitlines():
        if stripped_line := line.strip():
            yield stripped_line


def dutch(arr: List[int], pivot: int, left: int = 0, right: Optional[int] = None) -> Tuple[int, int]:
    if right is None:
        right = len(arr)
    low = left
    pos = left
    high = right - 1
    while pos <= high:
        v = arr[pos]
        if v < pivot:
            if pos == low:
                pos += 1
            else:
                arr[pos], arr[low] = arr[low], arr[pos]
            low += 1
        elif v == pivot:
            pos += 1
        else:
            arr[pos], arr[high] = arr[high], arr[pos]
            high -= 1
    return low, pos


def quick_select(arr: List[int], idx: int, left: int = 0, right: Optional[int] = None) -> int:
    if right is None:
        right = len(arr)
    if right - left <= 5:
        return sorted(arr[left:right])[idx]
    medians = [
        quick_select(arr, len(arr[idx : min(idx + 5, right)]) // 2, idx, min(idx + 5, right))
        for idx in range(left, right, 5)
    ]
    pivot = quick_select(medians, (len(medians) + 1) // 2)
    l, p = dutch(arr, pivot, left, right)
    if left + idx < l:
        return quick_select(arr, idx, left, l)
    if left + idx < p:
        return pivot
    return quick_select(arr, idx - p + left, p, right)


class SkaschSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        scores = []
        for line in parse(s):
            stack = []
            for char in line:
                if char in CLOSING:
                    stack.append(char)
                    continue
                left = stack.pop()
                if CLOSING[left] != char:
                    break
            else:
                score = 0
                while stack:
                    char = stack.pop()
                    value = POINTS[CLOSING[char]]
                    score = 5 * score + value
                scores.append(score)
        return quick_select(scores, len(scores) // 2)


def test_skasch() -> None:
    """
    Run `python -m pytest ./day-10/part-2/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""".strip()
        )
        == 288957
    )
