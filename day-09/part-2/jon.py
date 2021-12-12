from tool.runners.python import SubmissionPy
from collections import Counter


class JonSubmission(SubmissionPy):
    def run(self, s):
        m = s.strip().splitlines()

        ny = len(m)
        nx = len(m[0])

        def val(x, y):
            if x < 0 or x >= nx or y < 0 or y >= ny:
                return 10
            return int(m[y][x])

        bassin = {}

        for x in range(nx):
            for y in range(ny):
                v = val(x, y)
                if v < val(x-1, y) and v < val(x+1, y) and v < val(x, y-1) and v < val(x, y+1):
                    bassin[(x, y)] = (x, y)

        def get_bassin(x, y):
            v = val(x, y)
            if v >= 9:
                return None
            if (x, y) in bassin:
                return bassin[(x, y)]

            for mx, my in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                if val(mx, my) < v:
                    b = get_bassin(mx, my)
                    bassin[(x, y)] = b
                    return b

            raise Exception("No bassin found")

        for x in range(nx):
            for y in range(ny):
                get_bassin(x, y)

        sizes = sorted(Counter(bassin.values()).values())
        return sizes[-1] * sizes[-2] * sizes[-3]


def test_jon():
    """
    Run `python -m pytest ./day-09/part-2/jon.py` to test the submission.
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
        == 1134
    )
