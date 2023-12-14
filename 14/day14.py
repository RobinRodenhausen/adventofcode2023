import numpy as np

from functools import cache
from numpy.typing import NDArray
from typing import Any


def read_lines() -> list[str]:
    with open("14/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def parse_input() -> list[list[str]]:
    lines = read_lines()
    output = []

    for line in lines:
        tmp = []
        for s in line:
            tmp.append(s)
        output.append(tmp)

    return output


def part1():
    parsed = parse_input()
    plattform = np.flip(np.array(parsed, dtype=str).T, 1)
    total = 0

    # row: NDArray
    for row in plattform:
        # print("Row:", row)
        cubes = np.array([-1])
        cubes = np.append(cubes, np.where(row == "#")[0])
        cubes = np.append(cubes, len(row))
        rounds = np.where(row == "O")[0]
        for i in range(1, len(cubes)):
            upper = cubes[-i]
            # print("Upper", upper)
            lower = cubes[-i - 1]
            # print("Lower", lower)
            in_range = ((rounds > lower) & (rounds < upper)).sum()
            # print("Round in part", in_range)
            pos_clean = np.r_[lower + 1 : upper]
            row[pos_clean] = "."
            pos_fill = np.r_[upper - in_range : upper]
            row[pos_fill] = "O"
        # print(row)
        for x in np.where(row == "O")[0]:
            total += x + 1

    print(f"Total 1: {total}")


def roll_rocks(plattform: NDArray) -> NDArray:
    for row in plattform:
        # print("Row:", row)
        cubes = np.array([-1])
        cubes = np.append(cubes, np.where(row == "#")[0])
        cubes = np.append(cubes, len(row))
        rounds = np.where(row == "O")[0]
        for i in range(1, len(cubes)):
            upper = cubes[-i]
            # print("Upper", upper)
            lower = cubes[-i - 1]
            # print("Lower", lower)
            in_range = ((rounds > lower) & (rounds < upper)).sum()
            # print("Round in part", in_range)
            pos_clean = np.r_[lower + 1 : upper]
            row[pos_clean] = "."
            pos_fill = np.r_[upper - in_range : upper]
            row[pos_fill] = "O"
    return plattform


# Does not work because not hashable ...
# @cache
def rotate(plattform: NDArray) -> NDArray:
    # start at north
    plattform = roll_rocks(plattform)
    # rotate west
    plattform = np.rot90(plattform, axes=(1, 0))
    plattform = roll_rocks(plattform)
    # rotate south
    plattform = np.rot90(plattform, axes=(1, 0))
    plattform = roll_rocks(plattform)
    # rotate east
    plattform = np.rot90(plattform, axes=(1, 0))
    plattform = roll_rocks(plattform)
    # rotate north
    plattform = np.rot90(plattform, axes=(1, 0))
    return plattform


def hash_plattform(plattform: NDArray) -> int:
    return hash(tuple(["".join(row) for row in plattform]))


def calc_load(plattform: NDArray) -> int:
    total = 0
    for row in plattform:
        for x in np.where(row == "O")[0]:
            total += x + 1
    return total


def part2():
    stupid_big = 1000000000
    parsed = parse_input()
    plattform = np.flip(np.array(parsed, dtype=str).T, 1)
    hashes = []
    loads = []
    hash = 0
    for i in range(stupid_big):
        plattform = rotate(plattform)
        hash = hash_plattform(plattform)
        loads.append(calc_load(plattform))
        if hash in hashes:
            # print(i)
            # print(hash)
            break
        hashes.append(hash)

    cycle_begin = hashes.index(hash)
    cycle_length = len(hashes) - cycle_begin
    cycles_needed = (stupid_big - cycle_begin) % cycle_length + cycle_begin
    # print(cycles_needed)
    # print(loads)
    total = loads[cycles_needed - 1]

    print(f"Total 2: {total}")

    total = 0


if __name__ == "__main__":
    part1()
    part2()
