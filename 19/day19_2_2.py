import math
from itertools import groupby


class Workflow:
    id: str
    conditions: list[tuple[str, str]]

    def __init__(self, line: str) -> None:
        s1 = line.split("{")
        self.id = s1[0]
        self.conditions = []
        conditions = s1[1][:-1].split(",")
        for condition in conditions[:-1]:
            s2 = condition.split(":")
            self.conditions.append((s2[1], s2[0]))
        self.conditions.append((conditions[-1], ""))


def read_lines() -> list[str]:
    with open("19/input", "r") as f:
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


def negate_condition(condition: str):
    # No idea why it tries to double negate
    # if "=" in condition:
    #     return condition
    if condition[1] == "<":
        return condition[0] + ">=" + condition[2:]
    return condition[0] + "<=" + condition[2:]


def dfs(workflows: dict[str, Workflow], current: str, path: list = [], conditions: list = [], total=0) -> int:
    path = path + [current]
    if current == "R":
        return 0
    if current == "A":
        d = {key: [1, 4000] for key in ["x", "m", "a", "s"]}

        accepted_paths.append(path)
        # print(path)
        # print(conditions)
        for condition in conditions:
            cat = condition[0]
            if "=" in condition:
                op = condition[1:3]
                val = int(condition[3:])
            else:
                op = condition[1]
                val = int(condition[2:])

            if op == ">":
                d[cat][0] = val + 1
            elif op == ">=":
                d[cat][0] = val
            elif op == "<":
                d[cat][1] = val - 1
            else:
                d[cat][1] = val

        res = math.prod(k[1] - k[0] + 1 for k in d.values())
        # print(res)
        # print(d)
        return res

    next_conditions = conditions.copy()
    for i, (node, condition) in enumerate(workflows[current].conditions):
        if i > 0:
            tmp = conditions.copy()
            for con in next_conditions[len(conditions) : -1]:
                tmp.append(con)
            tmp.append(negate_condition(next_conditions[-1]))
            next_conditions = tmp
        if condition:
            next_conditions.append(condition)

        total += dfs(workflows, node, path, next_conditions)
    return total


if __name__ == "__main__":
    workflows = parse_input()
    accepted_paths = []
    total2 = dfs(workflows, "in")

    print(f"Total 2: {total2}")
    # example:167409079868000 - full:126107942006821
    assert total2 == 167409079868000 or total2 == 126107942006821
    # Finally found the issue: Fucked up the parsing. Result is correct now. Cant be bothered to debug and fix the intital version
