import sys
from shapely.geometry import Point, Polygon


class Pipe:
    east: bool
    north: bool
    south: bool
    west: bool
    is_ground: bool
    is_start: bool
    x: int
    y: int
    steps_from_start: int
    is_part_of_loop: bool
    is_in_loop: bool

    def __init__(self, c: str, x: int, y: int) -> None:
        self._symbol = c
        self.x = x
        self.y = y
        self.east = False
        self.north = False
        self.south = False
        self.west = False
        self.is_ground = False
        self.is_start = False
        self.steps_from_start = sys.maxsize
        self.is_part_of_loop = False
        self.is_in_loop = False
        match c:
            case "|":
                self.south = True
                self.north = True
            case "-":
                self.east = True
                self.west = True
            case "L":
                self.east = True
                self.north = True
            case "J":
                self.north = True
                self.west = True
            case "7":
                self.south = True
                self.west = True
            case "F":
                self.east = True
                self.south = True
            case ".":
                self.is_ground = True
            case "S":
                self.is_start = True

    def __str__(self) -> str:
        return f"X:{self.x} Y:{self.y} N:{self.north} E:{self.east} S:{self.south} W:{self.west} L:{self.is_part_of_loop}"

    def get_connections(self) -> tuple[bool, bool, bool, bool]:
        return self.north, self.east, self.south, self.west


class Area:
    matrix: list[list[Pipe]]
    start: Pipe
    current: Pipe
    steps: int
    last_direction: str
    coords: list[tuple[int, int]]

    def __init__(self, matrix: list[list[Pipe]], start: Pipe) -> None:
        self.matrix = matrix
        self.start = start
        self.coords = []
        self.define_start()
        self.current = self.start
        self.steps = 0
        self.last_direction = ""

    def print(self):
        for y in self.matrix:
            line = ""
            for x in y:
                line += f"{x.steps_from_start if x.steps_from_start != sys.maxsize else '.'}"
            print(line)

    def print2(self):
        for y in self.matrix:
            line = ""
            for x in y:
                if x.is_part_of_loop:
                    s = "*"
                elif x.is_in_loop:
                    s = "I"
                else:
                    s = x._symbol
                line += s
            print(line)

    def define_start(self):
        # check north
        if self.start.y > 0:
            north = self.matrix[self.start.y - 1][self.start.x]
            if north.south:
                self.start.north = True
        # check east
        if self.start.x < len(self.matrix[0]) - 1:
            east = self.matrix[self.start.y][self.start.x + 1]
            if east.west:
                self.start.east = True
        # check south
        if self.start.y < len(self.matrix) - 1:
            south = self.matrix[self.start.y + 1][self.start.x]
            if south.north:
                self.start.south = True
        # check west
        if self.start.x > 0:
            west = self.matrix[self.start.y][self.start.x - 1]
            if west.east:
                self.start.west = True

        self.start.steps_from_start = 0
        self.start.is_part_of_loop = True
        self.coords.append((self.start.x, self.start.y))

    def next(self) -> bool:
        north, east, south, west = self.current.get_connections()
        self.steps += 1
        # print(self.current)
        if north and self.last_direction != "S":
            self.current = self.matrix[self.current.y - 1][self.current.x]
            self.last_direction = "N"
            # print("North")
        elif east and self.last_direction != "W":
            self.current = self.matrix[self.current.y][self.current.x + 1]
            self.last_direction = "E"
            # print("East")
        elif south and self.last_direction != "N":
            self.current = self.matrix[self.current.y + 1][self.current.x]
            self.last_direction = "S"
            # print("South")
        elif west and self.last_direction != "E":
            self.current = self.matrix[self.current.y][self.current.x - 1]
            self.last_direction = "W"
            # print("West")

        self.current.is_part_of_loop = True

        if self.current.steps_from_start > self.steps:
            self.current.steps_from_start = self.steps

        self.coords.append((self.current.x, self.current.y))

        return not self.current == self.start and self.steps != 0

    def reverse_next(self) -> bool:
        north, east, south, west = self.current.get_connections()
        self.steps += 1
        # print(self.current)
        if west and self.last_direction != "E":
            self.current = self.matrix[self.current.y][self.current.x - 1]
            self.last_direction = "W"
            # print("West")
        elif south and self.last_direction != "N":
            self.current = self.matrix[self.current.y + 1][self.current.x]
            self.last_direction = "S"
            # print("South")
        elif east and self.last_direction != "W":
            self.current = self.matrix[self.current.y][self.current.x + 1]
            self.last_direction = "E"
            # print("East")
        elif north and self.last_direction != "S":
            self.current = self.matrix[self.current.y - 1][self.current.x]
            self.last_direction = "N"
            # print("North")

        self.current.is_part_of_loop = True

        if self.current.steps_from_start > self.steps:
            self.current.steps_from_start = self.steps

        return not self.current == self.start and self.steps != 0

    def get_highest_distance(self) -> int:
        total = 0
        for y in self.matrix:
            for x in y:
                if x.steps_from_start > total and x.steps_from_start != sys.maxsize:
                    total = x.steps_from_start
        return total


def read_lines() -> list[str]:
    with open("10/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def parse_input() -> Area:
    matrix: list[list[Pipe]] = []
    lines = read_lines()
    for li, line in enumerate(lines):
        matrix.append([])
        for ci, c in enumerate(line):
            matrix[li].append(Pipe(c, ci, li))
            if matrix[li][ci].is_start:
                start = matrix[li][ci]

    return Area(matrix, start)  # pyright:ignore[reportUnboundVariable]


def part1():
    area = parse_input()
    while area.next():
        pass
    area.last_direction = ""
    area.steps = 0
    while area.reverse_next():
        pass

    print(f"Total 1: {area.get_highest_distance()}")


def part2():
    area = parse_input()
    while area.next():
        pass

    coords = []
    for y in area.matrix:
        for x in y:
            if x.is_part_of_loop:
                coords.append((x.x, x.y))

    poly = Polygon(area.coords)

    total = 0
    for y in area.matrix:
        for x in y:
            p = Point(x.x, x.y)
            if poly.contains(p):
                x.is_in_loop = True
                total += 1
    # area.print2()

    print(f"Total 2: {total}")


if __name__ == "__main__":
    part1()
    part2()
