from tool.runners.python import SubmissionPy


class JulesdtSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        last = None
        count = 0
        for line in s.split():
            nb = int(line)
            if last is None:
                last = nb
                continue
            if nb > last:
                count += 1
            last = nb
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
