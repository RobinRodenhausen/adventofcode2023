from dataclasses import dataclass


@dataclass
class Draw:
    red: int
    green: int
    blue: int

    def is_possible(self) -> bool:
        return self.red <= 12 and self.green <= 13 and self.blue <= 14


class Bag:
    def __init__(self, line: str) -> None:
        self.draws: list[Draw] = []
        s1 = line.split(":")
        self.game_id = int(s1[0].split(" ")[-1])
        s2 = s1[1].split(";")
        for draw in s2:
            colors = [s.strip() for s in draw.split(",")]
            red, green, blue = 0, 0, 0
            for color in colors:
                s3 = color.split(" ")
                cube_amount = int(s3[0])
                cube_color = s3[1]
                if cube_color == "red":
                    red = cube_amount
                elif cube_color == "green":
                    green = cube_amount
                elif cube_color == "blue":
                    blue = cube_amount
            self.draws.append(Draw(red=red, green=green, blue=blue))

        self.is_possible = True
        for draw in self.draws:
            if not draw.is_possible():
                self.is_possible = False
                return

    def get_minimum(self):
        red, green, blue = 0, 0, 0
        for draw in self.draws:
            if draw.red > red:
                red = draw.red
            if draw.green > green:
                green = draw.green
            if draw.blue > blue:
                blue = draw.blue

        return red * green * blue


def read_lines() -> list[str]:
    with open("02/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def part1():
    bags: list[Bag] = []
    lines = read_lines()
    for line in lines:
        bags.append(Bag(line))

    total = 0
    for bag in bags:
        if bag.is_possible:
            total += bag.game_id

    print(f"Total 1 {total}")


def part2():
    bags: list[Bag] = []
    lines = read_lines()
    for line in lines:
        bags.append(Bag(line))

    total = 0
    for bag in bags:
        total += bag.get_minimum()

    print(f"Total 2 {total}")


if __name__ == "__main__":
    part1()
    part2()
