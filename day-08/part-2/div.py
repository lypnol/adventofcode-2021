from tool.runners.python import SubmissionPy

from collections import defaultdict


class DivSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        lines = s.split("\n")
        return sum(self.decode_segments(line) for line in lines)
        # return self.decode_segments(lines[1])

    def decode_segments(self, line):
        left, right = line.split(" | ")

        length_to_patterns = defaultdict(set)
        for group in left.split(" "):
            length_to_patterns[len(group)].add("".join(sorted(group)))

        digit_to_segments = [None] * 10
        digit_to_segments[1] = length_to_patterns[2].pop()
        digit_to_segments[7] = length_to_patterns[3].pop()
        digit_to_segments[4] = length_to_patterns[4].pop()
        digit_to_segments[8] = length_to_patterns[7].pop()

        assert digit_to_segments[8] == "abcdefg"

        for pattern in length_to_patterns[5]:
            # it can be 2, 3, or 5
            s = set(pattern)
            # it is a 3 if and only if it contains all the segments of the 7
            if all(x in s for x in digit_to_segments[7]):
                digit_to_segments[3] = pattern
            # it is a 2 if and only if the segments + the segments for the 4 are all the segments
            elif len(s | set(digit_to_segments[4])) == 7:
                digit_to_segments[2] = pattern
            else:
                digit_to_segments[5] = pattern

        for pattern in length_to_patterns[6]:
            # if can be 0, 6, or 9
            s = set(pattern)
            # it is a 9 if and only if it contains all the segments of the 4
            if all(x in s for x in digit_to_segments[4]):
                digit_to_segments[9] = pattern
            elif all(x in s for x in digit_to_segments[1]):
                digit_to_segments[0] = pattern
            else:
                digit_to_segments[6] = pattern

        segments_to_digit = {x: i for i, x in enumerate(digit_to_segments)}

        number = ""
        for group in right.split(" "):
            g = "".join(sorted(group))
            number += str(segments_to_digit[g])

        print(number)
        return int(number)


def test_div():
    """
    Run `python -m pytest ./day-08/part-1/div.py` to test the submission.
    """
    assert (
        DivSubmission().run(
            """
""".strip()
        )
        == None
    )
