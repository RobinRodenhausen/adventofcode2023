import itertools
from math import gcd


class Node:
    key: str
    left: str
    right: str

    def __init__(self, input: str) -> None:
        s1 = input.split("=")
        self.key = s1[0].strip()
        s2 = s1[1].split(",")
        self.left = s2[0][-3:]
        self.right = s2[1].strip()[:3]

    def __str__(self) -> str:
        return f"{self.key} -> L:{self.left} R:{self.right}"

    def get_next(self, direction: str) -> str:
        if direction == "L":
            return self.left
        elif direction == "R":
            return self.right
        raise ValueError("Invalid direction")


def read_lines() -> list[str]:
    with open("08/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def parse_input() -> tuple[str, dict]:
    node_list: list[Node] = []
    lines = read_lines()
    directions = lines[0]
    for line in lines[2:]:
        node_list.append(Node(line))

    nodes = {}
    for node in node_list:
        nodes[node.key] = node

    return directions, nodes


def part1():
    directions, nodes = parse_input()
    key = "AAA"
    total = 0
    for c_dir in itertools.cycle(directions):
        total += 1
        key = nodes[key].get_next(c_dir)

        if key == "ZZZ":
            print(f"Total 1: {total}")
            return


# Brute Force - Does take way too long
# After 10 minutes it was at ~300.000.000
# Correct result is at 24.035.773.251.517 and would take ~556 days
def part2():
    directions, nodes = parse_input()
    start_keys = [key for key in nodes.keys() if key[-1] == "A"]
    print(start_keys)
    total = 0

    for c_dir in itertools.cycle(directions):
        total += 1
        if total % 1000000 == 0:
            print(total)
        next_keys = []
        for key in start_keys:
            next_keys.append(nodes[key].get_next(c_dir))

        if all(key[-1] == "Z" for key in next_keys):
            print(f"Total 2: {total}")
            return

        start_keys = next_keys


# Caluclate each way separately and get the least common multiple
def part2_2():
    directions, nodes = parse_input()
    start_keys = [key for key in nodes.keys() if key[-1] == "A"]
    print(start_keys)

    result_map = {}

    for key in start_keys:
        start_key = key
        tmp = 0
        for c_dir in itertools.cycle(directions):
            tmp += 1
            key = nodes[key].get_next(c_dir)

            if key[-1] == "Z":
                result_map[start_key] = tmp
                break

    total = 1
    print(result_map)
    for key in result_map.keys():
        total = total * result_map[key] // gcd(total, result_map[key])

    print(f"Total 2: {total}")


if __name__ == "__main__":
    part1()
    part2_2()
