from tool.runners.python import SubmissionPy

from collections import defaultdict


class ThChSubmission(SubmissionPy):
    def explore(self, connections, small_cave_twice, current_path,
                current_cave):
        if current_cave == "end":
            return [current_path]

        current_path.append(current_cave)

        paths = []
        for next_cave in connections[current_cave]:
            is_small_cave = next_cave.islower()
            if next_cave == "start":
                continue

            new_small_cave_twice = small_cave_twice
            if is_small_cave and next_cave in current_path:
                if small_cave_twice:
                    continue
                new_small_cave_twice = next_cave

            paths += self.explore(connections, new_small_cave_twice,
                                  current_path[:], next_cave)

        return paths

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        connections = defaultdict(set)
        for line in s.splitlines():
            from_cave, to_cave = line.split("-")
            connections[from_cave].add(to_cave)
            connections[to_cave].add(from_cave)

        return len(self.explore(connections, None, [], "start"))


def test_th_ch():
    """
    Run `python -m pytest ./day-12/part-1/th-ch.py` to test the submission.
    """
    assert (ThChSubmission().run("""
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""".strip()) == 36)
