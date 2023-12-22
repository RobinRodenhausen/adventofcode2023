from collections import defaultdict


def read_lines() -> list[str]:
    with open("22/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def parse_input() -> list[tuple[int, int, int, int, int, int]]:
    lines = read_lines()
    bricks: list[tuple[int, int, int, int, int, int]] = []
    for line in lines:
        c1, c2 = line.split("~")
        x1, y1, z1 = map(int, c1.split(","))
        x2, y2, z2 = map(int, c2.split(","))

        bricks.append((x1, y1, z1, x2, y2, z2))

    return bricks


# Check input data
def debug_brick(brick: tuple[int, int, int, int, int, int]):
    print(brick)
    x1, y1, z1, x2, y2, z2 = brick
    if x1 != x2 and y1 != y2:
        # No matches -> Only one coord (x or y) changes
        print("Square")
    if z1 > z2:
        # No matches -> First coord is always the lowest point)
        print("Z Order")
    if z2 > z1:
        # Some matches -> There are vertical bricks
        print("Vertical Z")


def drop_brick(
    brick: tuple[int, int, int, int, int, int], max_z: defaultdict[tuple[int, int], int]
) -> tuple[int, int, int, int, int, int]:
    x1, y1, z1, x2, y2, z2 = brick
    settle_z = max(max_z[(x, y)] for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)) + 1  # +1 fall on top and not same place
    fall_distance = z1 - settle_z
    return (x1, y1, z1 - fall_distance, x2, y2, z2 - fall_distance)


def settle(bricks: list[tuple[int, int, int, int, int, int]]) -> tuple[list[tuple[int, int, int, int, int, int]], int]:
    max_z: defaultdict[tuple[int, int], int] = defaultdict(int)
    settled_bricks: list[tuple[int, int, int, int, int, int]] = []
    falls = 0
    for brick in bricks:
        dropped_brick = drop_brick(brick, max_z)
        if dropped_brick[2] != brick[2]:
            falls += 1
        settled_bricks.append(dropped_brick)
        x1, y1, _, x2, y2, z2 = dropped_brick
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                max_z[(x, y)] = z2
    return settled_bricks, falls


def part1():
    bricks = parse_input()
    total = 0
    # sort by lowest point -> z1
    bricks.sort(key=lambda brick: brick[2])
    settled_bricks, _ = settle(bricks)
    for i, brick in enumerate(settled_bricks):
        # Remove brick from settled bricks without changing the original structure
        copy = settled_bricks[:i] + settled_bricks[i + 1 :]
        # Settle again, if bricks fall it was carrying another one
        _, falls = settle(copy)
        # print(falls)
        if falls == 0:
            total += 1

    print(f"Total 1: {total}")


def part2():
    bricks = parse_input()
    total = 0
    # sort by lowest point -> z1
    bricks.sort(key=lambda brick: brick[2])
    settled_bricks, _ = settle(bricks)
    for i, brick in enumerate(settled_bricks):
        # Remove brick from settled bricks without changing the original structure
        copy = settled_bricks[:i] + settled_bricks[i + 1 :]
        # Settle again, if bricks fall it was carrying another one
        _, falls = settle(copy)
        # print(falls)
        if falls != 0:
            total += falls

    print(f"Total 2: {total}")


if __name__ == "__main__":
    part1()
    part2()
