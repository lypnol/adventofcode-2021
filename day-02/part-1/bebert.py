from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):
    def run(self, s):
        position = 0
        depth = 0
        for line in s.splitlines():
            lsplit = line.split(" ")
            instr = lsplit[0]
            amount = int(lsplit[1])
            if instr == "forward":
                position += amount
            elif instr == "down":
                depth += amount
            elif instr == "up":
                depth -= amount
        return position * depth


def test_bebert():
    """
    Run `python -m pytest ./day-02/part-1/bebert.py` to test the submission.
    """
    assert BebertSubmission().run("""
""".strip()) == 0
