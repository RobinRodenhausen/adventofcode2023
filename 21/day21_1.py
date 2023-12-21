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
    if li > 0 and garden[li - 1][ci]:
        neighbors.append((li - 1, ci))
    # south
    if li < len(garden) - 1 and garden[li + 1][ci]:
        neighbors.append((li + 1, ci))
    # west
    if ci > 0 and garden[li][ci - 1]:
        neighbors.append((li, ci - 1))
    # east
    if ci < len(garden[0]) - 1 and garden[li][ci + 1]:
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


def part1():
    garden, start = parse_input()
    print(start)

    # example
    # queue: list[tuple[tuple[int, int], int]] = [(start, 6)]
    queue: list[tuple[tuple[int, int], int]] = [(start, 64)]
    visisted = set()
    while queue:
        current, steps = queue.pop(0)
        queue += traverse(garden, current, steps, visisted)

        # print(len(queue))
    debug_garden(garden, start, target)

    # print(visisted)
    total = len(target)
    print(f"Total 1: {total}")
    assert total == 3746 or total == 16


if __name__ == "__main__":
    part1()
