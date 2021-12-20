import functools
from typing import List, Tuple

import numpy as np
import numpy.typing as npt
from tool.runners.python import SubmissionPy

Array = npt.NDArray[np.int_]

PAD_DEPTH = 2


def pad(image: Array, border: int) -> Array:
    pad_top = 1 if any(v != border for v in image[PAD_DEPTH - 1, :]) else 0
    pad_bot = 1 if any(v != border for v in image[-PAD_DEPTH, :]) else 0
    pad_left = 1 if any(v != border for v in image[:, PAD_DEPTH - 1]) else 0
    pad_right = 1 if any(v != border for v in image[:, -PAD_DEPTH]) else 0
    return np.pad(
        image, ((pad_top, pad_bot), (pad_left, pad_right)), constant_values=border
    )


def parse(s: str) -> Tuple[List[int], Array]:
    lines_iter = iter(s.splitlines())
    algorithm_str = next(lines_iter)
    algorithm = [1 if c == "#" else 0 for c in algorithm_str.strip()]
    image = []
    for line in lines_iter:
        if stripped_line := line.strip():
            image.append([1 if c == "#" else 0 for c in stripped_line])
    return algorithm, np.array(image)


TIMES = 2


class SkaschSubmission(SubmissionPy):
    @functools.lru_cache(None)
    def encode(
        self,
        im00: int,
        im01: int,
        im02: int,
        im10: int,
        im11: int,
        im12: int,
        im20: int,
        im21: int,
        im22: int,
    ) -> int:
        return self.algorithm[
            256 * im00
            + 128 * im01
            + 64 * im02
            + 32 * im10
            + 16 * im11
            + 8 * im12
            + 4 * im20
            + 2 * im21
            + im22
        ]

    def conv(self, image: Array, border: int) -> Tuple[Array, int]:
        new_border = self.algorithm[0] if border == 0 else self.algorithm[-1]
        res = np.full_like(image, new_border)
        for c in range(1, image.shape[1] - 1):
            for r in range(1, image.shape[0] - 1):
                res[r, c] = self.encode(
                    image[r - 1, c - 1],
                    image[r - 1, c],
                    image[r - 1, c + 1],
                    image[r, c - 1],
                    image[r, c],
                    image[r, c + 1],
                    image[r + 1, c - 1],
                    image[r + 1, c],
                    image[r + 1, c + 1],
                )
        return res, new_border

    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        self.encode.cache_clear()
        self.algorithm, image = parse(s)
        border = 0
        image = pad(image, border)
        for _ in range(TIMES):
            image = pad(image, border)
            image, border = self.conv(image, border)
        return image.sum()


def test_skasch() -> None:
    """
    Run `python -m pytest ./day-20/part-1/skasch.py` to test the submission.
    """
    assert (
        SkaschSubmission().run(
            """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
""".strip()
        )
        == 3351
    )
