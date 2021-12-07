from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    @staticmethod
    def distance(x, y):
        n = abs(y - x)
        return n * (n + 1) // 2

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        crabs = [int(crab) for crab in s.split(",")]
        avg = round(sum(crabs) / len(crabs))
        best_score = sum(self.distance(crab, avg) for crab in crabs)

        has_burst_best_score = False
        offset = -1
        while not has_burst_best_score:
            score = sum(self.distance(crab, avg + offset) for crab in crabs)
            if score > best_score:
                has_burst_best_score = True
            else:
                best_score = score
            offset -= 1

        has_burst_best_score = False
        offset = 1
        while not has_burst_best_score:
            score = sum(self.distance(crab, avg + offset) for crab in crabs)
            if score > best_score:
                has_burst_best_score = True
            else:
                best_score = score
            offset += 1

        return best_score


def test_th_ch():
    """
    Run `python -m pytest ./day-07/part-2/th-ch.py` to test the submission.
    """
    assert (ThChSubmission().run("""
16,1,2,0,4,2,7,1,2,14
""".strip()) == 168)
