from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        lines = s.splitlines()

        remaining = lines
        current_index = 0
        while len(remaining) > 1:
            nb_zeros = sum(line[current_index] == '0' for line in remaining)
            nb_ones = sum(line[current_index] == '1' for line in remaining)
            bit = '1' if nb_ones >= nb_zeros else '0'
            remaining = [
                line for line in remaining if line[current_index] == bit
            ]
            current_index += 1
        oxygen_generator_rating = remaining[0]

        remaining = lines
        current_index = 0
        while len(remaining) > 1:
            nb_zeros = sum(line[current_index] == '0' for line in remaining)
            nb_ones = sum(line[current_index] == '1' for line in remaining)
            bit = '0' if nb_zeros <= nb_ones else '1'
            remaining = [
                line for line in remaining if line[current_index] == bit
            ]
            current_index += 1
        co2_scrubber_rating = remaining[0]

        return int(oxygen_generator_rating, 2) * int(co2_scrubber_rating, 2)


def test_th_ch():
    """
    Run `python -m pytest ./day-03/part-2/th-ch.py` to test the submission.
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
""".strip()) == 230)
