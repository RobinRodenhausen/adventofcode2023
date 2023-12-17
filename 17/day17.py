#################
#               #
# DOES NOT WORK #
#               #
#################


import heapq
from pprint import pprint


def read_lines() -> list[str]:
    with open("17/input_t", "r") as f:
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


def heuristic(a: tuple[int, ...], b: tuple[int, ...]):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(blocks: list[list[int]], start: tuple[int, int, int, int, int], goal: tuple[int, int]) -> tuple[dict, dict]:
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[(start[0], start[1])] = None
    cost_so_far[(start[0], start[1])] = 0

    current: tuple[int, int, int, int, int]

    while priority_queue:
        _, current = heapq.heappop(priority_queue)
        if current[0] == goal[0] and current[1] == goal[1]:
            break
        for next in neighbors(blocks, current):
            if 0 <= next[0] < len(blocks) and 0 <= next[1] < len(blocks[0]):
                continue
            new_cost = cost_so_far[(current[0], current[1])] + blocks[next[0]][next[1]]
            if (next[0], next[1]) not in cost_so_far or new_cost < cost_so_far[(next[0], next[1])]:
                cost_so_far[(next[0], next[1])] = new_cost
                priority = new_cost + heuristic(goal, next)
                heapq.heappush(priority_queue, (priority, next))
                came_from[(next[0], next[1])] = (current[0], current[1])

    return came_from, cost_so_far


def neighbors(blocks: list[list[int]], current: tuple[int, int, int, int, int]) -> list[tuple[int, int, int, int, int]]:
    # vy, vx, streak
    directions: list[tuple[int, int, int]] = []
    # moving right
    if current[2] == 1 and current[4] < 3:
        directions.append((0, 1, current[4] + 1))
        directions.append((1, 0, 1))
        directions.append((-1, 0, 1))
    # moving left
    if current[2] == -1 and current[4] < 3:
        directions.append((0, -1, current[4] + 1))
        directions.append((1, 0, 1))
        directions.append((-1, 0, 1))
    # moving up
    if current[3] == -1 and current[4] < 3:
        directions.append((-1, 0, current[4] + 1))
        directions.append((0, 1, 1))
        directions.append((0, -1, 1))
    # moving down
    if current[3] == 1 and current[4] < 3:
        directions.append((1, 0, current[4] + 1))
        directions.append((0, 1, 1))
        directions.append((0, -1, 1))

    result: list[tuple[int, int, int, int, int]] = []
    for dir in directions:
        nx, ny = current[0] + dir[0], current[1] + dir[1]
        if 0 <= nx < len(blocks[0]) and 0 <= ny < len(blocks):
            result.append((nx, ny, dir[0], dir[1], dir[2]))
    return result


def part1():
    blocks = parse_input()
    # line, column, v_line, v_column, streak
    # y, x, vy, vx, streak
    start: tuple[int, int, int, int, int] = (0, 0, 0, 1, 0)
    goal: tuple[int, int] = (len(blocks[0]) - 1, len(blocks) - 1)

    came_from, cost_so_far = astar(blocks, start, goal)

    # print(came_from)
    # print("###")
    # print(cost_so_far)

    current = goal
    path = []
    while current[0] != start[0] and current[1] != start[1]:
        path.append(current)
        current = came_from[current]
        path.append(start)
        path.reverse()
    print(path)

    for x in cost_so_far.keys():
        if x[0] == goal[0] and x[1] == goal[1]:
            print(cost_so_far[x])


if __name__ == "__main__":
    part1()
