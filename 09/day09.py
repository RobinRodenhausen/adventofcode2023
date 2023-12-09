class Sequence:
    sequence: list[int]
    has_next: bool
    next: "Sequence"

    def __init__(self, line: str) -> None:
        self.sequence = [int(s) for s in line.split()]

        if all(i == 0 for i in self.sequence):
            self.has_next = False
        else:
            self.has_next = True
            self.next = Sequence(self.gen_next())

    def __str__(self) -> str:
        return f"{self.sequence}  {'-> ' + str(self.next) if self.has_next else ''}"

    def gen_next(self) -> str:
        tmp: list[int] = []
        for i in range(len(self.sequence) - 1):
            tmp.append(self.sequence[i + 1] - self.sequence[i])
        return " ".join(str(i) for i in tmp)

    def get_next_value(self) -> int:
        if not self.has_next:
            return 0
        else:
            return self.sequence[-1] + self.next.get_next_value()

    def get_previous_value(self) -> int:
        if not self.has_next:
            return 0
        else:
            return self.sequence[0] - self.next.get_previous_value()


def read_lines() -> list[str]:
    with open("09/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def parse_input() -> list[Sequence]:
    sequence_list: list[Sequence] = []
    lines = read_lines()
    for line in lines:
        sequence_list.append(Sequence(line))

    return sequence_list


def part1():
    sequences = parse_input()
    total = 0
    for seq in sequences:
        total += seq.get_next_value()

    print(f"Total 1: {total}")


def part2():
    sequences = parse_input()
    total = 0
    for seq in sequences:
        total += seq.get_previous_value()

    print(f"Total 2: {total}")


if __name__ == "__main__":
    part1()
    part2()
