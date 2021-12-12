from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):
    def run(self, s):
        m = s.strip().splitlines()

        ny = len(m)
        nx = len(m[0])

        def val(x, y):
            if x < 0 or x >= nx or y < 0 or y >= ny:
                return 10
            return int(m[y][x])

        risk = 0
        for x in range(nx):
            for y in range(ny):
                v = val(x, y)
                if v < val(x-1, y) and v < val(x+1, y) and v < val(x, y-1) and v < val(x, y+1):
                    risk += 1 + v

        return risk


def test_jon():
    """
    Run `python -m pytest ./day-09/part-1/jon.py` to test the submission.
    """
    assert (
        JonSubmission().run(
            """
2199943210
3987894921
9856789892
8767896789
9899965678
""".strip()
        )
        == 15
    )
