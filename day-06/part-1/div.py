from tool.runners.python import SubmissionPy


class DivSubmission(SubmissionPy):
    DAYS = 80
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here

        # in the following array, we store at index i the number of lanternfish createdd
        # by a lanternfish creates the first lanternfish (number 0) i days before self.DAYS
        created_by_lasting_day = [None]*self.DAYS

        created_by_lasting_day[0] = 0 # a lanternfish with 0 days remaining will create one the following day, so it's 0
        # for the next 7 days, the lanternfish will create 1 another lanternfish that won't create anyother one, so the value is 1
        for day in range(1,8):
            created_by_lasting_day[day] = 1

        # for day=8, the original lanternfish will create 2 lanternfish : one between day 7 and 8, and one between day 0 and 1
        created_by_lasting_day[8] = 2
        for day in range(9,self.DAYS):
            # we can start the recursion now!
            # the number of lanternsfish created is:
            # + the number of lanternfish the same lanternsfish will create in 7 days
            # + 1 (the one being created)
            # + the number of lanternfish the child will create (so at days +9)
            created_by_lasting_day[day] = 1 + created_by_lasting_day[day-7] + created_by_lasting_day[day-9]

        # now let's count
        statuses = [int(x) for x in s.split(",")]

        result = len(statuses)
        for x in statuses:
            result += created_by_lasting_day[self.DAYS-x]

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
