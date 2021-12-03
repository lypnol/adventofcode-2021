from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):
    def run(self, s):
        all_numbers = [line.strip() for line in s.splitlines()]
        line_length = len(all_numbers[0])

        oxygen_numbers = [line.strip() for line in s.splitlines()]
        oxygen_rating = 0
        for i in range(line_length):
            local_counts = {'0': 0, '1': 0}
            for line in oxygen_numbers:
                local_counts[line[i]] += 1
            most_common = '1' if local_counts['1'] >= local_counts['0'] else '0'
            oxygen_numbers = [n for n in oxygen_numbers if n[i] == most_common]
            if len(oxygen_numbers) == 1:
                oxygen_rating = int(oxygen_numbers[0], 2)

        co2_numbers = [line.strip() for line in s.splitlines()]
        co2_rating = 0
        for i in range(line_length):
            local_counts = {'0': 0, '1': 0}
            for line in co2_numbers:
                local_counts[line[i]] += 1
            least_common = '1' if local_counts['1'] < local_counts['0'] else '0'
            co2_numbers = [n for n in co2_numbers if n[i] == least_common]
            if len(co2_numbers) == 1:
                co2_rating = int(co2_numbers[0], 2)

        return oxygen_rating * co2_rating
