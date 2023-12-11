from __future__ import annotations
from itertools import combinations


class Galaxy:
    x: int
    y: int
    id: int
    galaxies: list[tuple[Galaxy, int]]
    total_distance: int

    def __init__(self, x: int, y: int, id: int) -> None:
        self.x = x
        self.y = y
        self.id = id
        self.galaxies = []
        self.total_distance = 0

    def __str__(self) -> str:
        return f"ID:{self.id} X:{self.x} Y:{self.y} - {len(self.galaxies)}:{self.total_distance}"

    def add_galaxy(self, galaxy: Galaxy, distance: int):
        self.galaxies.append((galaxy, distance))
        self.total_distance += distance


def read_lines() -> list[str]:
    with open("11/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def parse_input() -> list[Galaxy]:
    lines = read_lines()
    universe: list[str] = []
    galaxies: list[Galaxy] = []

    c_index: list[int] = []
    # empty columns
    for i in range(len(lines[0])):
        if all(line[i] == "." for line in lines):
            c_index.append(i)

    lines2: list[str] = []
    c_index.reverse()

    for line in lines:
        for i in c_index:
            line = line[:i] + "." + line[i:]
        lines2.append(line)

    # empty lines
    for line in lines2:
        # print(line)
        universe.append(line)
        if line == len(line) * line[0]:
            universe.append(line)

    i = 1
    for yi, y in enumerate(universe):
        for xi, x in enumerate(y):
            if x == "#":
                galaxies.append(Galaxy(x=xi, y=yi, id=i))
                i += 1

    return galaxies


def part1():
    galaxies = parse_input()

    for g1, g2 in combinations(galaxies, 2):
        x_diff = abs(g1.x - g2.x)
        y_diff = abs(g1.y - g2.y)
        distance = x_diff + y_diff
        g1.add_galaxy(g2, distance)

    total = 0
    for galaxy in galaxies:
        # print(galaxy)
        total += galaxy.total_distance

    print(f"Total 1: {total}")


def parse_input2(multi: int) -> list[Galaxy]:
    lines = read_lines()
    galaxies: list[Galaxy] = []

    c_index: list[int] = []
    l_index: list[int] = []
    # empty columns
    for i in range(len(lines[0])):
        if all(line[i] == "." for line in lines):
            c_index.append(i)

    # empty lines
    for li, line in enumerate(lines):
        if line == len(line) * line[0]:
            l_index.append(li)

    i = 1
    # multi = 1000000
    # add the multiplier to the coordinates for every expansion that is between (0,0) and the galaxy
    # subtract the amount of expansions since it is replaced and not added
    for yi, y in enumerate(lines):
        for xi, x in enumerate(y):
            if x == "#":
                multi_x = sum(xi > i for i in c_index)
                if multi_x > 0:
                    multi_x = multi_x * multi - multi_x
                multi_y = sum(yi > i for i in l_index)
                if multi_y > 0:
                    multi_y = multi_y * multi - multi_y
                galaxies.append(Galaxy(x=xi + multi_x, y=yi + multi_y, id=i))
                i += 1

    return galaxies


# part1 again with logic for part2
def part1_1():
    galaxies = parse_input2(2)

    for g1, g2 in combinations(galaxies, 2):
        x_diff = abs(g1.x - g2.x)
        y_diff = abs(g1.y - g2.y)
        distance = x_diff + y_diff
        g1.add_galaxy(g2, distance)

    total = 0
    for galaxy in galaxies:
        # print(galaxy)
        total += galaxy.total_distance

    print(f"Total 1: {total}")


def part2():
    galaxies = parse_input2(1000000)

    for g1, g2 in combinations(galaxies, 2):
        x_diff = abs(g1.x - g2.x)
        y_diff = abs(g1.y - g2.y)
        distance = x_diff + y_diff
        g1.add_galaxy(g2, distance)

    total = 0
    for galaxy in galaxies:
        # print(galaxy)
        total += galaxy.total_distance

    print(f"Total 2: {total}")


if __name__ == "__main__":
    part1()
    part1_1()
    part2()
