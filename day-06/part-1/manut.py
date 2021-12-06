from tool.runners.python import SubmissionPy


class ManutSubmission(SubmissionPy):
    def run(self, s):
        f = s.split('\n')[0].split(',')
        days = 80
        # print(f)
        simulation = [0,0,0,0,0,0,0,0,0]
        day0 = 0
        for i in f:
            simulation[int(i)] = simulation[int(i)] + 1
        for i in range(days):
            newOne = simulation[day0]
            day0 += 1
            if day0 == 9:
                day0 = 0
            simulation[day0+6 if day0 <= 2 else day0-3] += newOne
            # print(day0)
            # for i in range(9):
            #     print(str((i)%9) + ":"+str(simulation[(i+day0) %9]))
            # print()
        return sum(simulation)


def test_manut():
    """
    Run `python -m pytest ./day-06/part-1/manut.py` to test the submission.
    """
    assert (
        ManutSubmission().run(
            """
""".strip()
        )
        == None
    )
