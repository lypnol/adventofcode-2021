from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):
    def run(self, s):
        all_lines = [line.strip() for line in s.splitlines()]
        line_length = len(all_lines[0])

        counts = [{'0': 0, '1': 0} for _ in range(line_length)]
        for line in all_lines:
            for i, x in enumerate(line):
                counts[i][x] += 1

        gamma = 0
        epsilon = 0
        for i in range(line_length):
            most_common = 1 if counts[i]['1'] > counts[i]['0'] else 0
            least_common = 1 - most_common
            p = 2 ** (line_length - i - 1)
            gamma += most_common * p
            epsilon += least_common * p
        return gamma * epsilon
