def read_lines() -> list[str]:
    with open("15/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def parse_input() -> list[str]:
    lines = read_lines()
    return lines[0].split(",")


def calc_hash(s: str) -> int:
    tmp = 0
    for c in s:
        tmp += ord(c)
        tmp *= 17
        tmp = tmp % 256
    return tmp


def part1():
    init = parse_input()
    total = 0

    for step in init:
        total += calc_hash(step)

    print(f"Total 1: {total}")


def part2():
    init = parse_input()
    boxes = {}
    for i in range(256):
        boxes[i] = {}

    for step in init:
        if "=" in step:
            s1 = step.split("=")
            box = calc_hash(s1[0])
            boxes[box][s1[0]] = int(s1[1])
        if "-" in step:
            box = calc_hash(step[:-1])
            try:
                del boxes[box][step[:-1]]
            except KeyError:
                pass
    # print(boxes)

    total = 0
    for box in boxes.keys():
        for slot, bkey in enumerate(boxes[box].keys()):
            total += (box + 1) * (slot + 1) * boxes[box][bkey]

    print(f"Total 2: {total}")


if __name__ == "__main__":
    part1()
    part2()
