from itertools import groupby


class Part:
    x: int
    m: int
    a: int
    s: int

    def __init__(self, line: str) -> None:
        self.x = None  # pyright: ignore[reportGeneralTypeIssues]
        self.m = None  # pyright: ignore[reportGeneralTypeIssues]
        self.a = None  # pyright: ignore[reportGeneralTypeIssues]
        self.s = None  # pyright: ignore[reportGeneralTypeIssues]
        sp1 = line[1:-1].split(",")
        for p in sp1:
            sp2 = p.split("=")
            match sp2[0]:
                case "x":
                    self.x = int(sp2[1])
                case "m":
                    self.m = int(sp2[1])
                case "a":
                    self.a = int(sp2[1])
                case "s":
                    self.s = int(sp2[1])


class Workflow:
    id: str
    conditions: list[tuple[str, str]]

    def __init__(self, line: str) -> None:
        s1 = line.split("{")
        self.id = s1[0]
        self.conditions = []
        conditions = s1[1][:-1].split(",")
        for condition in conditions[:-1]:
            # print(condition)
            s2 = condition.split(":")
            # condition, result
            self.conditions.append((s2[0], s2[1]))
        self.conditions.append(("True", conditions[-1]))

        # print("ID:", self.id)
        # print("Con:", self.conditions)

    def __str__(self) -> str:
        return f"{self.id}"

    def __expr__(self) -> str:
        return self.__str__()

    def evaluate(self, part: Part) -> str:
        x = part.x
        m = part.m
        a = part.a
        s = part.s
        for condition in self.conditions:
            # print(condition[0])
            if eval(condition[0]):
                return condition[1]
        raise ValueError("No condition matches")

    def evaluate2(self, x: int, m: int, a: int, s: int) -> str:
        for condition in self.conditions:
            if eval(condition[0]):
                return condition[1]
        raise ValueError("No condition matches")


def read_lines() -> list[str]:
    with open("19/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def parse_input() -> tuple[dict[str, Workflow], list[Part]]:
    lines = read_lines()
    input = [list(group) for k, group in groupby(lines, lambda x: x == "") if not k]

    workflows: dict[str, Workflow] = {}
    parts: list[Part] = []

    w_lines = input[0]
    for w_line in w_lines:
        w = Workflow(w_line)
        workflows[w.id] = w
    p_lines = input[1]
    for p_line in p_lines:
        parts.append(Part(p_line))

    return workflows, parts


def part1():
    workflows, parts = parse_input()
    total = 0
    for part in parts:
        curr = "in"
        while curr != "R" and curr != "A":
            curr = workflows[curr].evaluate(part)

        if curr == "A":
            total += part.x + part.m + part.a + part.s

    print(f"Total 1: {total}")


if __name__ == "__main__":
    part1()
