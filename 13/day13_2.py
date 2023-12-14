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


def get_mirror_index(matrix: NDArray[Any]) -> list[int]:
    results = []
    for i in range(1, len(matrix)):
        if (matrix[i] == matrix[i - 1]).all():
            if is_full_mirror(matrix, i):
                results.append(i)
    # print(results)
    return results


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


def brute_force(pattern: list[list[str]]) -> list[int]:
    # print(pattern)
    totals = []
    matrix = numpy.array(pattern)
    for i in get_mirror_index(matrix):
        totals.append(i * 100)
    r_matrix = numpy.rot90(matrix, axes=(1, 0))
    for i in get_mirror_index(r_matrix):
        totals.append(i)
    return totals


def part2():
    patterns = parse_input()
    total1 = 0
    total2 = 0

    for pattern in patterns:
        original = brute_force(pattern)[0]
        total1 += original

        tmp = 0
        for yi, y in enumerate(pattern):
            for xi, x in enumerate(y):
                # Flip one symbol at a time
                if pattern[yi][xi] == ".":
                    pattern[yi][xi] = "#"
                else:
                    pattern[yi][xi] = "."

                flipped = brute_force(pattern)

                for i in flipped:
                    if i != original:
                        # print("i", i)
                        # print("o", original)
                        tmp = i
                        break
                if tmp != 0:
                    break

                # Flip back if no mirror
                if pattern[yi][xi] == ".":
                    pattern[yi][xi] = "#"
                else:
                    pattern[yi][xi] = "."
            if tmp != 0:
                break
        total2 += tmp

    print(f"Total 1: {total1}")
    print(f"Total 2: {total2}")


if __name__ == "__main__":
    part2()
