from tool.runners.python import SubmissionPy


class DivSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        state = [int(x) for x in s.split(",")]
        for day in range(80):
            n = len(state)
            for i in range(n):
                if state[i] == 0:
                    state[i] = 6
                    state.append(8)
                elif state[i] > 0:
                    state[i] -= 1

        return len(state)

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
