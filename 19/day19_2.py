import math
from itertools import groupby


class Workflow:
    id: str
    conditions: dict[str, str]

    def __init__(self, line: str) -> None:
        s1 = line.split("{")
        self.id = s1[0]
        self.conditions = {}
        conditions = s1[1][:-1].split(",")
        for condition in conditions[:-1]:
            s2 = condition.split(":")
            self.conditions[s2[1]] = s2[0]
        self.conditions[conditions[-1]] = ""
        pass


def read_lines() -> list[str]:
    with open("19/input_e", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def parse_input() -> dict[str, Workflow]:
    lines = read_lines()
    input = [list(group) for k, group in groupby(lines, lambda x: x == "") if not k]

    workflows: dict[str, Workflow] = {}

    w_lines = input[0]
    for w_line in w_lines:
        w = Workflow(w_line)
        workflows[w.id] = w

    return workflows


def dfs(workflows: dict[str, Workflow], current: str, path: list = []):
    if current == "R":
        return
    if current == "A":
        # path = path + ["A"]
        # print(path)
        accepted_paths.append(path)
        return
    for node in workflows[current].conditions.keys():
        # if len(workflows[current].conditions[node]) > 0:
        #     cat = node
        # else:
        #     cat = ""

        tmp_path = path + [f"{current}:{node}"]
        dfs(workflows, node, tmp_path)


if __name__ == "__main__":
    workflows = parse_input()
    accepted_paths = []
    dfs(workflows, "in")
    total2 = 0
    for path in accepted_paths:
        d = {key: [1, 4000] for key in ["x", "m", "a", "s"]}
        print(path)
        for node in path:
            workflow, next = node.split(":")
            for c_key in workflows[workflow].conditions.keys():
                condition = workflows[workflow].conditions[c_key]
                if condition:
                    type = condition[0]
                    op = condition[1]
                    val = int(condition[2:])
                    if op == ">" and c_key == next:
                        d[type][0] = val + 1
                    elif op == "<" and not c_key == next:
                        d[type][0] = val
                    elif op == "<" and c_key == next:
                        d[type][1] = val - 1
                    else:
                        d[type][1] = val
                if c_key == next:
                    break
        total2 += math.prod(k[1] - k[0] + 1 for k in d.values())

    print(f"Total 2: {total2}")
    assert total2 == 167409079868000
    # Does work for the example, but doesn't work for the actual input. I am tired of debugging this garbage
    # Fucked up the parsing in the first place ... Different and working approach in 19_2_2.py
