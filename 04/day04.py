from dataclasses import dataclass


def read_lines() -> list[str]:
    with open("04/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def part1():
    lines = read_lines()
    total = 0
    for line in lines:
        s1 = line.split(":")[1]
        s2 = s1.split("|")
        winning = [int(s) for s in s2[0].strip().split()]
        have = [int(s) for s in s2[1].strip().split()]

        points = 0
        for w in winning:
            if w in have:
                if points == 0:
                    points = 1
                else:
                    points *= 2
        total += points

    print(f"Total 1: {total}")


@dataclass
class Card:
    winning: list[int]
    have: list[int]
    amount: int


def part2():
    lines = read_lines()
    total = 0
    cards: list[Card] = []

    for line in lines:
        s1 = line.split(":")[1]
        s2 = s1.split("|")
        winning = [int(s) for s in s2[0].strip().split()]
        have = [int(s) for s in s2[1].strip().split()]
        cards.append(Card(winning=winning, have=have, amount=1))

    for ci, card in enumerate(cards):
        n = 0
        for w in card.winning:
            if w in card.have:
                n += 1

        for i in range(1, n + 1):
            if ci + i < len(cards):
                cards[ci + i].amount += 1 * card.amount

    for card in cards:
        total += card.amount

    print(f"Total 2: {total}")


if __name__ == "__main__":
    part1()
    part2()
