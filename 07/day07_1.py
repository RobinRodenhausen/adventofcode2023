import collections
import re


def read_lines() -> list[str]:
    with open("07/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


class Hand:
    _cards: str
    cards: list[int]
    bet: int
    hand_rank: int

    def __init__(self, cards: str, bet: int) -> None:
        self.bet = bet
        self._cards = cards
        self.cards = []
        for c in self._cards:
            self.cards.append(self.card_to_int(c))

        self.hand_rank = self.get_hand_rank()

    def __str__(self) -> str:
        return f"Card:{self._cards} Bet:{self.bet} CardInt:{self.cards} HandRank:{self.hand_rank}"

    def __eq__(self, other) -> bool:
        return self._cards == other._cards

    def __lt__(self, other) -> bool:
        if self.hand_rank == other.hand_rank:
            for i, v in enumerate(self.cards):
                if v == other.cards[i]:
                    continue
                else:
                    return v < other.cards[i]
        return self.hand_rank < other.hand_rank

    def card_to_int(self, c: str) -> int:
        if re.match(r"\d", c):
            return int(c)
        match c:
            case "T":
                return 10
            case "J":
                return 11
            case "Q":
                return 12
            case "K":
                return 13
            case "A":
                return 14
        raise ValueError("Card parsing failed")

    def is_five(self) -> bool:
        if len(collections.Counter(self.cards).keys()) == 1:
            return True
        return False

    def is_four(self) -> bool:
        d = collections.Counter(self.cards)
        for key in d.keys():
            if d[key] == 4:
                return True
        return False

    def is_full_house(self) -> bool:
        d = collections.Counter(self.cards)
        if len(d.keys()) == 2:
            for key in d.keys():
                if d[key] == 2 or d[key] == 3:
                    return True
        return False

    def is_three(self) -> bool:
        d = collections.Counter(self.cards)
        if len(d.keys()) == 3:
            for key in d.keys():
                if d[key] == 3:
                    return True
        return False

    def is_two_pair(self) -> bool:
        d = collections.Counter(self.cards)
        if len(d.keys()) == 3:
            # Normally not enough for a check, but since is_three is checked first it is the only other option
            return True
        return False

    def is_pair(self) -> bool:
        d = collections.Counter(self.cards)
        if len(d.keys()) == 4:
            return True
        return False

    def get_hand_rank(self) -> int:
        if self.is_five():
            return 7
        if self.is_four():
            return 6
        if self.is_full_house():
            return 5
        if self.is_three():
            return 4
        if self.is_two_pair():
            return 3
        if self.is_pair():
            return 2
        return 1


def parse_input() -> list[Hand]:
    hands: list[Hand] = []
    lines = read_lines()
    for line in lines:
        s = line.split()
        hands.append(Hand(cards=s[0], bet=int(s[1])))
    return hands


def part1():
    hands = parse_input()
    hands.sort()
    total = 0
    for i, hand in enumerate(hands):
        total += (i + 1) * hand.bet

    print(f"Total 1: {total}")


if __name__ == "__main__":
    part1()
