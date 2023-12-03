import re
import uuid

from dataclasses import dataclass, field
from pprint import pprint


@dataclass
class Number:
    counted: bool
    value: int
    uid: uuid.UUID = field(init=False)

    def __post_init__(self):
        self.uid: uuid.UUID = uuid.uuid4()


def read_lines() -> list[str]:
    with open("03/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def fill_matrix(lines: list[str]) -> list[list[str]]:
    matrix: list[list[str]] = []
    for li, line in enumerate(lines):
        matrix.append([])
        for c in line:
            matrix[li].append(c)
    return matrix


def fill_matrix_with_number(matrix: list[list[str]]) -> list[list[str | Number]]:
    matrix2: list[list[str | Number]] = []
    for li, line in enumerate(matrix):
        matrix2.append([])
        for ci, c in enumerate(line):
            matrix2[li].append(c)

        number_matches = re.finditer(r"\d+", "".join(line))
        for number in number_matches:
            start_i = number.start()
            end_i = number.end()
            n = Number(value=int(number.group()), counted=False)
            for i in range(start_i, end_i):
                matrix2[li][i] = n
    return matrix2


def count1(matrix: list[list[str | Number]]) -> int:
    total = 0

    for li, line in enumerate(matrix):
        for ci, c in enumerate(line):
            # Only check surroding if number
            if isinstance(c, Number):
                # Skip if already counted
                if c.counted:
                    continue
                # left
                if ci > 0 and isinstance(matrix[li][ci - 1], str) and matrix[li][ci - 1] != ".":
                    total += c.value
                    c.counted = True
                # right
                if ci < len(line) - 1 and isinstance(matrix[li][ci + 1], str) and matrix[li][ci + 1] != ".":
                    total += c.value
                    c.counted = True
                # up
                if li > 0 and isinstance(matrix[li - 1][ci], str) and matrix[li - 1][ci] != ".":
                    total += c.value
                    c.counted = True
                # down
                if li < len(matrix) - 1 and isinstance(matrix[li + 1][ci], str) and matrix[li + 1][ci] != ".":
                    total += c.value
                    c.counted = True
                # leftup
                if ci > 0 and li > 0 and isinstance(matrix[li - 1][ci - 1], str) and matrix[li - 1][ci - 1] != ".":
                    total += c.value
                    c.counted = True
                # leftdown
                if ci > 0 and li < len(matrix) - 1 and isinstance(matrix[li + 1][ci - 1], str) and matrix[li + 1][ci - 1] != ".":
                    total += c.value
                    c.counted = True
                # rightup
                if ci < len(line) - 1 and li > 0 and isinstance(matrix[li - 1][ci + 1], str) and matrix[li - 1][ci + 1] != ".":
                    total += c.value
                    c.counted = True
                # rightdown
                if (
                    ci < len(line) - 1
                    and li < len(matrix) - 1
                    and isinstance(matrix[li + 1][ci + 1], str)
                    and matrix[li + 1][ci + 1] != "."
                ):
                    total += c.value
                    c.counted = True
    return total


def count2(matrix: list[list[str | Number]]) -> int:
    total = 0

    for li, line in enumerate(matrix):
        for ci, c in enumerate(line):
            # Only check surroding if number
            if isinstance(c, Number):
                # Skip if already counted
                if c.counted:
                    continue
                # left
                if ci > 0 and isinstance(matrix[li][ci - 1], str) and matrix[li][ci - 1] != ".":
                    if matrix[li][ci - 1] == "*":
                        total += gear(li=li, ci=ci - 1, matrix=matrix)
                    else:
                        pass
                        # total += c.value
                    c.counted = True
                # right
                if ci < len(line) - 1 and isinstance(matrix[li][ci + 1], str) and matrix[li][ci + 1] != ".":
                    if matrix[li][ci + 1] == "*":
                        total += gear(li=li, ci=ci + 1, matrix=matrix)
                    else:
                        pass
                        # total += c.value
                    c.counted = True
                # up
                if li > 0 and isinstance(matrix[li - 1][ci], str) and matrix[li - 1][ci] != ".":
                    if matrix[li - 1][ci] == "*":
                        total += gear(li=li - 1, ci=ci, matrix=matrix)
                    else:
                        pass
                        # total += c.value
                    c.counted = True
                # down
                if li < len(matrix) - 1 and isinstance(matrix[li + 1][ci], str) and matrix[li + 1][ci] != ".":
                    if matrix[li + 1][ci] == "*":
                        total += gear(li=li + 1, ci=ci, matrix=matrix)
                    else:
                        pass
                        # total += c.value
                    c.counted = True
                # leftup
                if ci > 0 and li > 0 and isinstance(matrix[li - 1][ci - 1], str) and matrix[li - 1][ci - 1] != ".":
                    if matrix[li - 1][ci - 1] == "*":
                        total += gear(li=li - 1, ci=ci - 1, matrix=matrix)
                    else:
                        pass
                        # total += c.value
                    c.counted = True
                # leftdown
                if ci > 0 and li < len(matrix) - 1 and isinstance(matrix[li + 1][ci - 1], str) and matrix[li + 1][ci - 1] != ".":
                    if matrix[li + 1][ci - 1] == "*":
                        total += gear(li=li + 1, ci=ci - 1, matrix=matrix)
                    else:
                        pass
                        # total += c.value
                    c.counted = True
                # rightup
                if ci < len(line) - 1 and li > 0 and isinstance(matrix[li - 1][ci + 1], str) and matrix[li - 1][ci + 1] != ".":
                    if matrix[li - 1][ci + 1] == "*":
                        total += gear(li=li - 1, ci=ci + 1, matrix=matrix)
                    else:
                        pass
                        # total += c.value
                    c.counted = True
                # rightdown
                if (
                    ci < len(line) - 1
                    and li < len(matrix) - 1
                    and isinstance(matrix[li + 1][ci + 1], str)
                    and matrix[li + 1][ci + 1] != "."
                ):
                    if matrix[li + 1][ci + 1] == "*":
                        total += gear(li=li + 1, ci=ci + 1, matrix=matrix)
                    else:
                        pass
                        # total += c.value
                    c.counted = True

    return total


def gear(li: int, ci: int, matrix: list[list[str | Number]]) -> int:
    total = 0
    numbers: list[Number] = []

    matrix_x = len(matrix[0]) - 1
    matrix_y = len(matrix) - 1

    # left
    if ci > 0 and isinstance(matrix[li][ci - 1], Number) and matrix[li][ci - 1] not in numbers:
        numbers.append(matrix[li][ci - 1])  # pyright: ignore[reportGeneralTypeIssues]
    # right
    if ci < matrix_x and isinstance(matrix[li][ci + 1], Number) and matrix[li][ci + 1] not in numbers:
        numbers.append(matrix[li][ci + 1])  # pyright: ignore[reportGeneralTypeIssues]
    # up
    if li > 0 and isinstance(matrix[li - 1][ci], Number) and matrix[li - 1][ci] not in numbers:
        numbers.append(matrix[li - 1][ci])  # pyright: ignore[reportGeneralTypeIssues]
    # down
    if li < matrix_y and isinstance(matrix[li + 1][ci], Number) and matrix[li + 1][ci] not in numbers:
        numbers.append(matrix[li + 1][ci])  # pyright: ignore[reportGeneralTypeIssues]
    # leftup
    if ci > 0 and li > 0 and isinstance(matrix[li - 1][ci - 1], Number) and matrix[li - 1][ci - 1] not in numbers:
        numbers.append(matrix[li - 1][ci - 1])  # pyright: ignore[reportGeneralTypeIssues]
    # leftdown
    if ci > 0 and li < matrix_y and isinstance(matrix[li + 1][ci - 1], Number) and matrix[li + 1][ci - 1] not in numbers:
        numbers.append(matrix[li + 1][ci - 1])  # pyright: ignore[reportGeneralTypeIssues]
    # rightup
    if ci < matrix_x and li > 0 and isinstance(matrix[li - 1][ci + 1], Number) and matrix[li - 1][ci + 1] not in numbers:
        numbers.append(matrix[li - 1][ci + 1])  # pyright: ignore[reportGeneralTypeIssues]
    # rightdown
    if ci < matrix_x and li < matrix_x and isinstance(matrix[li + 1][ci + 1], Number) and matrix[li + 1][ci + 1] not in numbers:
        numbers.append(matrix[li + 1][ci + 1])  # pyright: ignore[reportGeneralTypeIssues]
    if len(numbers) == 2:
        numbers[0].counted = True
        numbers[1].counted = True
        return numbers[0].value * numbers[1].value
    elif len(numbers) == 1:
        return 0
    else:
        raise ValueError("Something went wrong")


def part1():
    lines = read_lines()
    matrix = fill_matrix(lines)
    matrix2 = fill_matrix_with_number(matrix)

    print(f"Total 1: {count1(matrix2)}")


def part2():
    lines = read_lines()
    matrix = fill_matrix(lines)
    matrix2 = fill_matrix_with_number(matrix)

    print(f"Total 2: {count2(matrix2)}")


if __name__ == "__main__":
    part1()
    part2()
