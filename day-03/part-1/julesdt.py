from tool.runners.python import SubmissionPy


class JulesdtSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        lines = s.split()
        gamma = ""
        epsilon = ""
        for i in range(len(lines[0])):
            count = {"0": 0, "1":0}
            for j in range(len(lines)):
                count[lines[j][i]] += 1
            gamma += "0" if count["0"] > count["1"] else "1"
            epsilon += "1" if count["0"] > count["1"] else "0"
        return int(gamma, 2) * int(epsilon, 2)



def test_julesdt():
    """
    Run `python -m pytest ./day-03/part-1/julesdt.py` to test the submission.
    """
    assert (
        JulesdtSubmission().run(
            """
""".strip()
        )
        == None
    )
