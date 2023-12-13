import numpy

from numpy.typing import NDArray
from typing import Any

from itertools import groupby
from pprint import pprint


def read_lines() -> list[str]:
    with open("13/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def parse_input() -> list[list[list[str]]]:
    lines = read_lines()
    patterns = [list(group) for k, group in groupby(lines, lambda x: x == "") if not k]
    patterns = [[list(s) for s in pattern] for pattern in patterns]
    return patterns


def get_mirror_index(matrix: NDArray[Any]) -> int:
    for i in range(1, len(matrix)):
        if (matrix[i] == matrix[i - 1]).all():
            if is_full_mirror(matrix, i):
                return i

    # is not a (full) mirror
    return 0


def is_full_mirror(matrix: NDArray[Any], index: int) -> bool:
    max_reflect = min(index, len(matrix) - index)
    # start at 1 since this was already checked in the previous function
    for i in range(1, max_reflect):
        upper = index + i
        lower = index - i - 1
        # Only for debug
        # derp1 = "".join(list(matrix[upper]))
        # derp2 = "".join(list(matrix[lower]))
        if not (matrix[upper] == matrix[lower]).all():
            return False

    return True


def part1():
    patterns = parse_input()
    total = 0
    for pattern in patterns:
        matrix = numpy.array(pattern)
        total += get_mirror_index(matrix) * 100
        r_matrix = numpy.rot90(matrix, axes=(1, 0))
        total += get_mirror_index(r_matrix)

    print(f"Total 1: {total}")


def brute_force(pattern: list[list[str]]) -> int:
    # print(pattern)
    total = 0
    matrix = numpy.array(pattern)
    total += get_mirror_index(matrix) * 100
    r_matrix = numpy.rot90(matrix, axes=(1, 0))
    total += get_mirror_index(r_matrix)
    return total


def part2():
    patterns = parse_input()
    total = 0

    for pattern in patterns:
        original = brute_force(pattern)
        tmp = 0
        for yi, y in enumerate(pattern):
            for xi, x in enumerate(y):
                # Flip one symbol at a time
                if pattern[yi][xi] == ".":
                    pattern[yi][xi] = "#"
                else:
                    pattern[yi][xi] = "."

                flipped = brute_force(pattern)

                if flipped != original:
                    print(flipped)
                    tmp += flipped
                    break

                # Flip back if no mirror
                if pattern[yi][xi] == ".":
                    pattern[yi][xi] = "#"
                else:
                    pattern[yi][xi] = "."
            if tmp != 0:
                total += tmp
                break

    print(f"Total 2: {total}")


if __name__ == "__main__":
    part1()
