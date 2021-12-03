from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        lines = s.splitlines()
        sums = [0] * len(lines[0])
        for bit_nb in lines:
            for i, bit in enumerate(bit_nb):
                sums[i] += 1 if bit == '1' else 0
        half = len(lines) // 2
        gamma = ['1' if nb >= half else '0' for nb in sums]
        epsilon = ['1' if nb <= half else '0' for nb in sums]
        return int("".join(gamma), 2) * int("".join(epsilon), 2)


def test_th_ch():
    """
    Run `python -m pytest ./day-03/part-1/th-ch.py` to test the submission.
    """
    assert (ThChSubmission().run("""
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
""".strip()) == 198)
