from dataclasses import dataclass
from itertools import count


def read_lines() -> list[str]:
    with open("06/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


@dataclass
class Race:
    time: int
    distance: int

    def get_record_options(self) -> int:
        total = 0

        for i in count():
            speed = i
            distance = speed * (self.time - i)
            if distance > self.distance:
                low_limit = i
                high_limit = self.time + 1 - i
                total = high_limit - low_limit
                break

        return total


def parse_input1() -> list[Race]:
    lines = read_lines()
    times = [int(s) for s in lines[0].split(":")[1].split()]
    distances = [int(s) for s in lines[1].split(":")[1].split()]

    l: list[Race] = []
    for i, val in enumerate(times):
        l.append(Race(time=val, distance=distances[i]))

    return l


def parse_input2() -> Race:
    lines = read_lines()
    times = lines[0].split(":")[1].split()
    distances = lines[1].split(":")[1].split()

    return Race(time=int("".join(times)), distance=int("".join(distances)))


def part1():
    total = 1
    races = parse_input1()
    for r in races:
        total *= r.get_record_options()

    print(f"Total 1: {total}")


def part2():
    total = 0
    race = parse_input2()
    total = race.get_record_options()

    print(f"Total 2: {total}")


if __name__ == "__main__":
    part1()
    part2()
