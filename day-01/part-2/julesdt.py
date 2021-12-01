from tool.runners.python import SubmissionPy


class JulesdtSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        total = []
        count = 0
        for line in s.split():
            total.append(int(line))
            if len(total) < 4:
                continue
            # Faster than doing sums of sublists
            if total[1] + total[2] + total[3] > total[0] + total[1] + total[2]:
                count +=1
            total.pop(0)
        return count


def test_julesdt():
    """
    Run `python -m pytest ./day-01/part-1/julesdt.py` to test the submission.
    """
    assert (
        JulesdtSubmission().run(
            """
""".strip()
        )
        == None
    )
