import multiprocessing

from pprint import pprint
from dataclasses import dataclass


class Point:
    x: int
    y: int
    is_mirror: bool
    symbol: str
    is_energized: bool

    def __init__(self, x: int, y: int, symbol: str) -> None:
        self.x = x
        self.y = y
        self.symbol = symbol
        self.is_mirror = False if self.symbol == "." else True
        self.is_energized = False

    def __str__(self) -> str:
        return f"({self.x},{self.y}) - {self.symbol}"

    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class Light:
    x: int
    y: int
    vx: int
    vy: int

    # def __hash__(self) -> int:
    #     return hash((self.x, self.y, self.vx, self.vy))


@dataclass
class Grid:
    grid: list[list[Point]]
    visited: list[Light]

    def next(self, light: Light) -> list[Light]:
        # out of bounds
        if light.x < 0 or light.x >= len(self.grid[0]) or light.y < 0 or light.y >= len(self.grid):
            return []

        self.grid[light.y][light.x].is_energized = True
        # Already was here - loop detection
        if light in self.visited:
            return []
        else:
            self.visited.append(light)

        # splitter -
        if self.grid[light.y][light.x].symbol == "-" and light.vx == 0 and abs(light.vy) == 1:
            return [Light(x=light.x + 1, y=light.y, vx=1, vy=0), Light(x=light.x - 1, y=light.y, vx=-1, vy=0)]

        # splitter |
        if self.grid[light.y][light.x].symbol == "|" and abs(light.vx) == 1 and light.vy == 0:
            return [Light(x=light.x, y=light.y + 1, vx=0, vy=1), Light(x=light.x, y=light.y - 1, vx=0, vy=-1)]

        # mirror /
        # >
        if self.grid[light.y][light.x].symbol == "/" and light.vx == 1 and light.vy == 0:
            return [Light(x=light.x, y=light.y - 1, vx=0, vy=-1)]
        # <
        if self.grid[light.y][light.x].symbol == "/" and light.vx == -1 and light.vy == 0:
            return [Light(x=light.x, y=light.y + 1, vx=0, vy=1)]
        # v
        if self.grid[light.y][light.x].symbol == "/" and light.vx == 0 and light.vy == 1:
            return [Light(x=light.x - 1, y=light.y, vx=-1, vy=0)]
        # ^
        if self.grid[light.y][light.x].symbol == "/" and light.vx == 0 and light.vy == -1:
            return [Light(x=light.x + 1, y=light.y, vx=1, vy=0)]

        # mirror \
        # >
        if self.grid[light.y][light.x].symbol == "\\" and light.vx == 1 and light.vy == 0:
            return [Light(x=light.x, y=light.y + 1, vx=0, vy=1)]
        # <
        if self.grid[light.y][light.x].symbol == "\\" and light.vx == -1 and light.vy == 0:
            return [Light(x=light.x, y=light.y - 1, vx=0, vy=-1)]
        # v
        if self.grid[light.y][light.x].symbol == "\\" and light.vx == 0 and light.vy == 1:
            return [Light(x=light.x + 1, y=light.y, vx=1, vy=0)]
        # ^
        if self.grid[light.y][light.x].symbol == "\\" and light.vx == 0 and light.vy == -1:
            return [Light(x=light.x - 1, y=light.y, vx=-1, vy=0)]

        # empty space or ignore splitter
        # if grid[next_x][next_y] == ".":
        return [Light(x=light.x + light.vx, y=light.y + light.vy, vx=light.vx, vy=light.vy)]

    def reset(self):
        for y in self.grid:
            for x in y:
                x.is_energized = False
        self.visited.clear()

    def print(self):
        for line in self.grid:
            l = []
            for c in line:
                l.append("#" if c.is_energized else c.symbol)
            print("".join(l))

    def print2(self):
        for line in self.grid:
            l = []
            for c in line:
                l.append("#" if c.is_energized else ".")
            print("".join(l))


def read_lines() -> list[str]:
    with open("16/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def parse_input() -> Grid:
    lines = read_lines()
    grid: list[list[Point]] = []
    for li, line in enumerate(lines):
        grid.append([])
        for ci, c in enumerate(line):
            grid[li].append(Point(x=ci, y=li, symbol=c))

    return Grid(grid=grid, visited=[])


def part1():
    grid = parse_input()
    # grid.print()
    start = Light(x=0, y=0, vx=1, vy=0)
    positions: list[Light] = []
    positions.append(start)

    for p in positions:
        positions.extend(grid.next(p))
        # print("_____")
        # grid.print()

    # print("_____")
    # grid.print()

    # print("_____")
    # grid.print2()
    total = 0
    for y in grid.grid:
        for x in y:
            if x.is_energized:
                total += 1

    print(f"Total 1: {total}")


def part2():
    grid = parse_input()
    # grid.print()
    starts = []
    for y in range(len(grid.grid)):
        starts.append(Light(x=0, y=y, vx=1, vy=0))
        starts.append(Light(x=len(grid.grid[0]) - 1, y=y, vx=-1, vy=0))
    for x in range(len(grid.grid[0])):
        starts.append(Light(x=x, y=0, vx=0, vy=1))
        starts.append(Light(x=x, y=len(grid.grid) - 1, vx=0, vy=-1))

    # print(starts)

    # starts = [Light(x=3, y=0, vx=0, vy=1)]

    totals = []
    for start in starts:
        print(start)
        grid.reset()
        positions: list[Light] = []
        positions.append(start)

        for p in positions:
            positions.extend(grid.next(p))
            # print("_____")
            # grid.print()

        # print("_____")
        # grid.print()

        # print("_____")
        # grid.print2()
        total = 0
        for y in grid.grid:
            for x in y:
                if x.is_energized:
                    total += 1

        totals.append(total)

    # print(totals)
    print(f"Total 2: {max(totals)}")


def solve(positions: list[Light], grid: Grid, return_dict: dict, i: int):
    for p in positions:
        positions.extend(grid.next(p))
        # print("_____")
        # grid.print()

    # print("_____")
    # grid.print()

    # print("_____")
    # grid.print2()
    total = 0
    for y in grid.grid:
        for x in y:
            if x.is_energized:
                total += 1

    return_dict[i] = total


def part2_2():
    grid = parse_input()
    # grid.print()
    starts = []
    for y in range(len(grid.grid)):
        starts.append(Light(x=0, y=y, vx=1, vy=0))
        starts.append(Light(x=len(grid.grid[0]) - 1, y=y, vx=-1, vy=0))
    for x in range(len(grid.grid[0])):
        starts.append(Light(x=x, y=0, vx=0, vy=1))
        starts.append(Light(x=x, y=len(grid.grid) - 1, vx=0, vy=-1))

    # print(starts)

    # starts = [Light(x=3, y=0, vx=0, vy=1)]

    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    for i, start in enumerate(starts):
        print(i, start)
        grid.reset()
        positions: list[Light] = []
        positions.append(start)

        p = multiprocessing.Process(target=solve, args=(positions, Grid(grid=grid.grid.copy(), visited=[]), return_dict, i))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    print(return_dict.values())
    print(f"Total 2: {max(return_dict.values())}")

    # 7975 too low
    # 8023


if __name__ == "__main__":
    part1()
    part2_2()
