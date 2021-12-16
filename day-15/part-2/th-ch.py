from tool.runners.python import SubmissionPy

from queue import PriorityQueue


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        small_m = [[int(i) for i in line] for line in s.splitlines()]
        m = [[0 for i in range(5 * len(small_m))] for j in range(5 * len(small_m))]
        for x in range(len(small_m)):
            for y in range(len(small_m)):
                m[y][x] = small_m[y][x]
        for i in range(5):
            for j in range(5):
                if i == 0 and j == 0:
                    continue
                if i == 0:
                    for x in range(len(small_m)):
                        for y in range(len(small_m)):
                            m[len(small_m) * j + y][len(small_m) * i + x] = (
                                m[len(small_m) * (j - 1) + y][len(small_m) * i + x] + 1
                                if m[len(small_m) * (j - 1) + y][len(small_m) * i + x]
                                < 9
                                else 1
                            )
                else:
                    for x in range(len(small_m)):
                        for y in range(len(small_m)):
                            m[len(small_m) * j + y][len(small_m) * i + x] = (
                                m[len(small_m) * j + y][len(small_m) * (i - 1) + x] + 1
                                if m[len(small_m) * j + y][len(small_m) * (i - 1) + x]
                                < 9
                                else 1
                            )

        # Dijkstra with priority queue
        D = {(x, y): float("inf") for x in range(len(m)) for y in range(len(m))}
        D[(0, 0)] = 0

        pq = PriorityQueue()
        visited = set()
        pq.put((0, (0, 0)))

        while not pq.empty():
            (dist, (x, y)) = pq.get()
            visited.add((x, y))

            for (dx, dy) in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                if 0 <= x + dx < len(m) and 0 <= y + dy < len(m):
                    distance = m[y + dy][x + dx]
                    if (x + dx, y + dy) not in visited:
                        old_cost = D[(x + dx, y + dy)]
                        new_cost = D[(x, y)] + distance
                        if new_cost < old_cost:
                            pq.put((new_cost, (x + dx, y + dy)))
                            D[(x + dx, y + dy)] = new_cost
                            if x + dx == len(m) - 1 and y + dy == len(m) - 1:
                                return new_cost


def test_th_ch():
    """
    Run `python -m pytest ./day-15/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
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
        == 315
    )
