from functools import cache


def read_lines() -> list[str]:
    with open("12/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


# had to replace list[int] with tuple[int, ...] to make it hashable for cache in part 2
def parse_input() -> list[tuple[str, tuple[int, ...]]]:
    lines = read_lines()
    springs: list[tuple[str, tuple[int, ...]]] = []
    for line in lines:
        s1 = line.split()
        groups = tuple([int(s) for s in s1[1].split(",")])
        springs.append((s1[0], groups))
    return springs


# Do not recompute every time and use a cache for same calls. Learned about this during the elephant hell (day 16) last year ...
@cache
def count_arrangements(spring: str, groups: tuple[int, ...]) -> int:
    # If there is nothing left to check
    if len(spring) == 0:
        # and there are no groups left over
        if len(groups) == 0:
            return 1
        # otherwise it does not fit
        else:
            return 0
    # Ignore operational spring
    if spring.startswith("."):
        return count_arrangements(spring[1:], groups)
    # Replace corrupt data with both possibilities
    if spring.startswith("?"):
        return count_arrangements("." + spring[1:], groups) + count_arrangements("#" + spring[1:], groups)
    # If there is a broken spring
    if spring.startswith("#"):
        # If there are no more groups it doesn't fit
        if len(groups) == 0:
            return 0
        # If the expected group is larger than the rest of the string it doesn't fit
        if len(spring) < groups[0]:
            return 0
        # If there is an operational spring in the expected length it doesn't fit
        if "." in spring[: groups[0]]:
            return 0
        # If there is only one group left, the rest of the spring should not have any more groups left
        if len(groups) == 1:
            # cache does not like lists
            # return count_arrangements(spring[groups[0] :], [])
            return count_arrangements(spring[groups[0] :], ())
        if len(groups) > 1:
            # prevent string index out of range, if there is not enough space for an operational spring between groups
            if len(spring) < groups[0] + 1:
                return 0
            # There is no operational spring between groups
            if spring[groups[0]] == "#":
                return 0
            # There has to be an operational spring in between groups
            return count_arrangements(spring[groups[0] + 1 :], groups[1:])

    raise ValueError("Something went wrong. Good luck ...")


def part1():
    springs = parse_input()
    total = 0
    for spring in springs:
        # print(spring)

        total += count_arrangements(spring[0], spring[1])

    print(f"Total 1: {total}")


def part2():
    springs = parse_input()
    total = 0
    for spring in springs:
        # Multiply both sides by 5 and put a ? between the springs
        spring5 = ("?".join([spring[0]] * 5), spring[1] * 5)
        # print(spring5)

        total += count_arrangements(spring5[0], spring5[1])

    print(f"Total 2: {total}")


if __name__ == "__main__":
    part1()
    part2()
