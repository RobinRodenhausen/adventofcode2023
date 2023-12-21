import math
from functools import cache


def read_lines() -> list[str]:
    with open("21/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def parse_input() -> tuple[tuple[tuple[bool, ...], ...], tuple[int, int]]:
    lines = read_lines()
    tmp_garden: list[tuple[bool, ...]] = []
    start: tuple[int, int] = (-1, -1)
    for li, line in enumerate(lines):
        # garden.append([])
        l: list[bool] = []
        for ci, column in enumerate(line):
            # plot(.) = True
            if column == ".":
                l.append(True)
            # stone(#) = False
            elif column == "#":
                l.append(False)
            elif column == "S":
                l.append(True)
                start = (li, ci)
            else:
                raise ValueError(f"Invalid character {column} found")
        tmp_garden.append(tuple(l))

    garden = tuple(tmp_garden)

    if start == (-1, -1):
        raise ValueError("Start not found")

    return garden, start


def debug_garden(garden: tuple[tuple[bool, ...], ...], start: tuple[int, int], visisted: set):
    for li, line in enumerate(garden):
        l = ""
        for ci, column in enumerate(line):
            if (li, ci) == start:
                l += "S"
            elif (li, ci) in visisted:
                l += "O"
            elif column:
                l += "."
            else:
                l += "#"
        print(l)


@cache
def get_neighbors(garden: tuple[tuple[bool, ...], ...], point: tuple[int, int]) -> list[tuple[int, int]]:
    li, ci = point

    neighbors: list[tuple[int, int]] = []
    # north
    if garden[(li - 1) % len(garden)][ci % len(garden[0])]:
        neighbors.append((li - 1, ci))
    # south
    if garden[(li + 1) % len(garden)][ci % len(garden[0])]:
        neighbors.append((li + 1, ci))
    # west
    if garden[li % len(garden)][(ci - 1) % len(garden[0])]:
        neighbors.append((li, ci - 1))
    # east
    if garden[li % len(garden)][(ci + 1) % len(garden[0])]:
        neighbors.append((li, ci + 1))

    return neighbors


target = set()


def traverse(
    garden: tuple[tuple[bool, ...], ...], point: tuple[int, int], steps: int, visisted: set
) -> list[tuple[tuple[int, int], int]]:
    if (point, steps) in visisted:
        return []
    visisted.add((point, steps))

    if steps == 0:
        target.add(point)
        return []
    steps -= 1

    return [(n, steps) for n in get_neighbors(garden, point)]


def solve(garden: tuple[tuple[bool, ...], ...], start: tuple[int, int], steps: int) -> int:
    queue: list[tuple[tuple[int, int], int]] = [(start, steps)]
    visisted = set()
    while queue:
        current, steps = queue.pop(0)
        queue += traverse(garden, current, steps, visisted)

    total = len(target)
    # print(f"Total 2: {total}")
    return total


# def part2(steps: int, expected: int):
def part2():
    steps = 26501365
    garden, start = parse_input()

    height = len(garden)  # 131
    mod = steps % height  # 65

    print(mod)
    print(mod + height * 2)

    # r0 = solve(garden, start, mod) # 3889
    r0 = 3889
    print("65:", r0)
    # r1 = solve(garden, start, mod + height)  # 34504
    r1 = 34504
    print("196:", r1)
    # r2 = solve(garden, start, mod + height * 2)  # 95591
    r2 = 95591
    print("327:", r2)

    # Something something math. No clue what this does ... Something quadratic function
    m = r1 - r0
    print("m", m)
    n = r2 - r1
    print("n", n)
    a = (n - m) // 2
    print("a", a)
    b = m - 3 * a
    print("b", b)
    c = r0 - b - a
    print("c", c)

    ceiling = math.ceil(steps / height)

    total = a * ceiling**2 + b * ceiling + c

    print(total)
    # 623.540.829.615.589
    assert total == 623540829615589


if __name__ == "__main__":
    part2()
    # part2(6, 16)
    # part2(10, 50)
    # part2(50, 1594)
    # part2(100, 6536)
