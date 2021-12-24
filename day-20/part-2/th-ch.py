from tool.runners.python import SubmissionPy

from itertools import product


def get_surrounding_pixels(x, y):
    return [(x + dx, y + dy) for dy in [-1, 0, 1] for dx in [-1, 0, 1]]


def should_fallback(x, y, size_min, size_max):
    return not (size_min <= x < size_max and size_min <= y < size_max)


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        enhancement, grid = s.split("\n\n")
        light_pixels = set()
        default_pixel = "."
        size = 0
        for y, line in enumerate(grid.splitlines()):
            size = len(line)
            for x, char in enumerate(line):
                if char == "#":
                    light_pixels.add((x, y))

        for step in range(50):
            updated_light_pixels = set()
            for x, y in product(range(-1 - step, size + 1 + step), repeat=2):
                binary = ''.join([
                    '1' if (xx, yy) in light_pixels or
                    (should_fallback(xx, yy, -step, size + step)
                     and default_pixel == "#") else '0'
                    for (xx, yy) in get_surrounding_pixels(x, y)
                ])
                decimal = int(binary, 2)
                updated_pixel = enhancement[decimal]
                if updated_pixel == "#":
                    updated_light_pixels.add((x, y))
            light_pixels = updated_light_pixels

            if enhancement[0] == "#" and default_pixel == ".":
                default_pixel = "#"
            elif enhancement[511] == "." and default_pixel == "#":
                default_pixel = "."

        return len(light_pixels)


def test_th_ch():
    """
    Run `python -m pytest ./day-20/part-1/th-ch.py` to test the submission.
    """
    assert (ThChSubmission().run("""
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
""".strip()) == 3351)
