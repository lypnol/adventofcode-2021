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


def adjacent_points(arr, i, j):
    neighbours = []
    if i > 0 and arr[i - 1][j] != 9:
        neighbours.append((i - 1, j))
    if i < len(arr) - 1 and arr[i + 1][j] != 9:
        neighbours.append((i + 1, j))
    if j > 0 and arr[i][j - 1] != 9:
        neighbours.append((i, j - 1))
    if j < len(arr[0]) - 1 and arr[i][j + 1] != 9:
        neighbours.append((i, j + 1))
    return neighbours


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
        low_points = set()
        for i in range(n):
            for j in range(m):
                if is_low_point(arr, i, j):
                    low_points.add((i, j))

        areas = []
        for lp in low_points:
            neighbours = adjacent_points(arr, *lp)
            processed = set()
            while len(neighbours) > 0:
                n_p = neighbours.pop(0)
                if n_p in processed:
                    continue
                else:
                    neighbours.extend(adjacent_points(arr, *n_p))
                    processed.add(n_p)
            areas.append(len(processed))
        areas = sorted(areas)
        return areas[-1] * areas[-2] * areas[-3]


def test_youyoun():
    """
    Run `python -m pytest ./day-09/part-1/youyoun.py` to test the submission.
    """
    assert (YouyounSubmission().run("""2199943210
3987894921
9856789892
8767896789
9899965678""".strip()) == 1134)
