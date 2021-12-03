from tool.runners.python import SubmissionPy


class JulesdtSubmission(SubmissionPy):

    def get_value(self, lines, max_wanted=False):
        index = 0
        while len(lines) > 1:
            count = {"0": 0, "1":0}
            for i in range(len(lines)):
                count[lines[i][index]] += 1
            if max_wanted:
                bit = "0" if count["0"] > count["1"] else "1"
            else:
                bit = "0" if count["0"] <= count["1"] else "1"
            new_values = []
            for i in range(len(lines)):
                if lines[i][index] == bit:
                    new_values.append(lines[i])
            lines = new_values
            index += 1
        return lines[0]

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        lines = s.split()
        oxygen = self.get_value(lines[:], max_wanted=True)
        co2 = self.get_value(lines[:], max_wanted=False)
        return int(oxygen, 2) * int(co2, 2)


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
