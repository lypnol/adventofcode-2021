from tool.runners.python import SubmissionPy


def is_low_point(arr, i, j):
    if i > 0 and arr[i - 1][j] <= arr[i][j]:
        return False
    if i < len(arr) - 1 and arr[i + 1][j] <= arr[i][j]:
        return False
    if j > 0 and arr[i][j - 1] <= arr[i][j]:
        return False
    if j < len(arr[0]) - 1 and arr[i][j + 1] <= arr[i][j]:
        return False
    return True


class YouyounSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        arr = [list(map(int, list(x))) for x in s.splitlines()]
        n = len(arr)
        m = len(arr[0])
        r_level = 0
        for i in range(n):
            for j in range(m):
                if is_low_point(arr, i, j):
                    r_level += 1 + arr[i][j]
        return r_level


def test_youyoun():
    """
    Run `python -m pytest ./day-09/part-1/youyoun.py` to test the submission.
    """
    assert (YouyounSubmission().run("""2199943210
3987894921
9856789892
8767896789
9899965678""".strip()) == 15)
