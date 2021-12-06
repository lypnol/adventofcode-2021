from tool.runners.python import SubmissionPy


class DivSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        created_by_day = [None]*256 # if your first zero is at index i, how many lanternfish are created
        # for the last seven days, we know the answer, it's one (except the last day)
        for day in range(255-7,255):
            created_by_day[day] = 1
        created_by_day[255] = 0

        for day in range(255-7,-1,-1):
            created_by_day[day] = created_by_day[day+7]+1

        statuses = [int(x) for x in s.split(",")]

        result = len(statuses)
        for x in statuses:
            result += created_by_day[x]

        return result

def test_div():
    """
    Run `python -m pytest ./day-06/part-1/div.py` to test the submission.
    """
    assert (
        DivSubmission().run(
            """
""".strip()
        )
        == None
    )
