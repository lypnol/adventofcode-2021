import heapq

from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        cave = [[int(c) for c in line] for line in s.splitlines()]
        height, width = len(cave), len(cave[0])
        return a_star(cave, (0, 0), (height - 1, width - 1))


def a_star(cave, start, end):
    heuristic = lambda x: abs(end[0] - x[0]) + abs(end[1] - x[1])
    height, width = len(cave), len(cave[0])

    heap = [(heuristic(start), start, 0)]
    visited = set()
    while len(heap):
        _, node, dist = heapq.heappop(heap)

        if node == end:
            return dist

        if node in visited:
            continue

        visited.add(node)
        for neighbor in neighbors(*node, height, width):
            neighbor_dist = dist + cave[neighbor[0]][neighbor[1]]
            heapq.heappush(
                heap,
                (
                    neighbor_dist + heuristic(neighbor),
                    neighbor,
                    neighbor_dist,
                ),
            )

    return -1


def neighbors(i, j, height, width):
    for di, dj in [
        (-1, 0),
        (0, -1),
        (-1, -1),
        (1, 0),
        (0, 1),
    ]:
        (x, y) = (i + di, j + dj)
        if x >= 0 and y >= 0 and x < height and y < width:
            yield (x, y)


def test_thomren():
    """
    Run `python -m pytest ./day-15/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""".strip()
        )
        == 40
    )
