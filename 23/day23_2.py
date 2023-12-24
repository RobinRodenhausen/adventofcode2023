import sys

from functools import cache

sys.setrecursionlimit(100000)


def read_lines() -> list[str]:
    with open("23/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def parse_input() -> tuple[tuple[tuple[bool, ...], ...], tuple[int, int], tuple[int, int]]:
    lines = read_lines()
    tmp_trails: list[tuple[bool, ...]] = []
    start: tuple[int, int] = (-1, -1)
    goal: tuple[int, int] = (-1, -1)

    for li, line in enumerate(lines):
        l: list[bool] = []
        for ci, column in enumerate(line):
            if column == "#":
                l.append(False)
            else:
                l.append(True)

            if li == 0 and column == ".":
                start = (li, ci)
            if li == len(lines) - 1 and column == ".":
                goal = (li, ci)
        tmp_trails.append(tuple(l))

    trails = tuple(tmp_trails)

    if start == (-1, -1):
        raise ValueError("Start not found")
    if goal == (-1, -1):
        raise ValueError("Start not found")

    return trails, start, goal


@cache
def get_neighbors(trails: tuple[tuple[str, ...], ...], point: tuple[int, int]) -> list[tuple[int, int]]:
    li, ci = point
    neighbors: list[tuple[int, int]] = []
    # north
    if li > 0 and trails[li - 1][ci]:
        neighbors.append((li - 1, ci))
    # south
    if li < len(trails) - 1 and trails[li + 1][ci]:
        neighbors.append((li + 1, ci))
    # west
    if ci > 0 and trails[li][ci - 1]:
        neighbors.append((li, ci - 1))
    # east
    if ci < len(trails[0]) - 1 and trails[li][ci + 1]:
        neighbors.append((li, ci + 1))

    neighbors.reverse()
    return neighbors


def dfs(
    trails: tuple[tuple[bool, ...], ...],
    current: tuple[int, int],
    goal: tuple[int, int],
    results: list[int],
    visisted: set[tuple[int, int]] = None,  # pyright: ignore[reportGeneralTypeIssues]
    path: list[tuple[int, int]] = None,  # pyright: ignore[reportGeneralTypeIssues]
):
    if visisted is None:
        visisted = set()
    if path is None:
        path = []

    visisted.add(current)
    path = path + [current]

    if current == goal:
        path_length = len(path) - 1
        results.append(path_length)
        print(path_length)

    visisted.add(current)
    for n in get_neighbors(trails, current):
        if n not in visisted:
            dfs(trails, n, goal, results, visisted.copy(), path.copy())


def part2():
    trails, start, goal = parse_input()
    results: list[int] = []
    # Bring some time
    dfs(trails, start, goal, results)

    print(f"Total 2: {max(results)}")
    assert max(results) == 6490


if __name__ == "__main__":
    part2()
