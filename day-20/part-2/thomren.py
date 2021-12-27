from typing import Tuple

import numpy as np
import numpy.typing as npt
from scipy.signal import convolve2d

from tool.runners.python import SubmissionPy

NDArrayBool = npt.NDArray[np.bool_]
KERNEL = np.array([2 ** i for i in range(9)]).reshape((3, 3))


class ThomrenSubmission(SubmissionPy):
    def run(self, s, n_iter=2):
        """
        :param s: input in string format
        :return: solution flag
        """
        algorithm, image = parse_input(s)
        border = False
        for _ in range(n_iter):
            image = enhance(image, algorithm, border)
            # pprint_image(image)

            if algorithm[0] and not border:
                border = True
            elif not algorithm[-1] and border:
                border = False

        return image.sum()


def pprint_image(image):
    print("\n".join("".join("#" if x else "." for x in line) for line in image))


def parse_input(s: str) -> Tuple[NDArrayBool, NDArrayBool]:
    algorithm_str, image_str = s.split("\n\n")
    algorithm_str = algorithm_str.replace("\n", "")
    algorithm = np.array([1 if c == "#" else 0 for c in algorithm_str], dtype=bool)
    image = np.array(
        [[1 if c == "#" else 0 for c in line] for line in image_str.splitlines()]
    )
    return algorithm, image


def enhance(
    image: NDArrayBool, algorithm: NDArrayBool, border: bool = False
) -> NDArrayBool:
    values = convolve2d(image, KERNEL, fillvalue=border)
    return algorithm[values]


def test_thomren():
    """
    Run `python -m pytest ./day-20/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
""".strip()
        )
        == 35
    )
