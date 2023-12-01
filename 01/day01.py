import regex as re

numbers: dict = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def read_lines() -> list[str]:
    with open("01/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def part1():
    lines = read_lines()
    total = 0
    for line in lines:
        digits = re.findall(r"\d", line)
        total += int(digits[0] + digits[-1])
    print(f"Total Part 1: {total}")


def part2():
    lines = read_lines()
    adjusted_lines: list[str] = []
    total = 0
    for line in lines:
        matches: list[str] = re.findall(r"(one|two|three|four|five|six|seven|eight|nine|\d)", line, overlapped=True)
        for i, num in enumerate(matches):
            if num in numbers.keys():
                matches[i] = num.replace(num, numbers[num])

        digits = re.findall(r"\d", "".join(matches))
        total += int(digits[0] + digits[-1])

    print(f"Total Part 2: {total}")


if __name__ == "__main__":
    part1()
    part2()
