import heapq

from typing import Any, Generator


def read_lines() -> list[str]:
    with open("17/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def parse_input() -> list[list[int]]:
    lines = read_lines()
    blocks: list[list[int]] = []
    for li, line in enumerate(lines):
        blocks.append([])
        for column in line:
            blocks[li].append(int(column))

    return blocks


# return neighbors and cost of neighbor
def neighbors(
    blocks: list[list[int]], current: tuple[int, int, int, int, int]
) -> Generator[tuple[tuple[int, int, int, int, int], int], Any, Any]:
    (line, column, d_line, d_column, streak) = current

    # switch movement vector around x->y; y->x
    left, right = (-d_column, d_line), (d_column, -d_line)
    # neighbor below streak limit and not out of bounds
    if streak < 10 and 0 <= line + d_line < len(blocks) and 0 <= column + d_column < len(blocks[0]):
        yield (line + d_line, column + d_column, d_line, d_column, streak + 1), blocks[line + d_line][column + d_column]
    for d_line, d_column in left, right:
        # bounds check
        if 0 <= line + d_line < (len(blocks)) and 0 <= column + d_column < len(blocks[0]) and streak > 3:
            yield (line + d_line, column + d_column, d_line, d_column, 1), blocks[line + d_line][column + d_column]


def a_star(blocks: list[list[int]]):
    visisted = set()
    start1 = (0, 0, 1, 0, 0)
    start2 = (0, 0, 0, 1, 0)
    distances = {start1: 0, start2: 0}
    priority_queue = []
    heapq.heappush(priority_queue, (0, start1))
    heapq.heappush(priority_queue, (0, start2))
    goal = (len(blocks) - 1, len(blocks[0]) - 1)
    while priority_queue:
        _, current = heapq.heappop(priority_queue)
        if current in visisted:
            continue
        visisted.add(current)
        if current[:2] == goal and current[4] > 3:
            goal = current
            break
        for neighbor, cost in neighbors(blocks, current):
            if neighbor in visisted:
                continue
            new_cost = distances[current] + cost
            if neighbor not in distances or new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                heapq.heappush(priority_queue, (new_cost, neighbor))

    # print(distances)
    return distances[goal]


def part2():
    blocks = parse_input()
    print(f"Total 2: {a_star(blocks)}")


if __name__ == "__main__":
    part2()
