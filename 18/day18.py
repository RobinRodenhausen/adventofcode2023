import shapely


def read_lines() -> list[str]:
    with open("18/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def parse_input1() -> list[tuple[tuple[int, int], int]]:
    lines = read_lines()
    output: list[tuple[tuple[int, int], int]] = []
    for line in lines:
        s1 = line.split()
        match s1[0]:
            case "R":
                dir = (0, 1)
            case "D":
                dir = (1, 0)
            case "L":
                dir = (0, -1)
            case "U":
                dir = (-1, 0)
            case _:
                raise ValueError("No valid direction")

        dis = int(s1[1])
        output.append((dir, dis))

    return output


def part1():
    input = parse_input1()

    cur = (0, 0)
    coords: list[tuple[int, int]] = [cur]

    for i in input:
        d = (i[0][0] * i[1], i[0][1] * i[1])
        cur = (cur[0] + d[0], cur[1] + d[1])
        coords.append(cur)
        # print(cur)

    poly = shapely.Polygon(coords).buffer(0.5, join_style="mitre")
    print(f"Total 1: {int(poly.area)}")

    # Pick's theorem
    poly1 = shapely.Polygon(coords)
    print(f"Total 1_2: {int(poly1.area + poly1.length // 2 +1)}")


def parse_input2() -> list[tuple[tuple[int, int], int]]:
    lines = read_lines()
    output: list[tuple[tuple[int, int], int]] = []
    for line in lines:
        s1 = line.split()
        match s1[2][-2]:
            case "0":
                dir = (0, 1)
            case "1":
                dir = (1, 0)
            case "2":
                dir = (0, -1)
            case "3":
                dir = (-1, 0)
            case _:
                raise ValueError("No valid direction")

        # print(s1[2][2:-2])
        dis = int(s1[2][2:-2], 16)
        output.append((dir, dis))

    return output


def part2():
    input = parse_input2()

    cur = (0, 0)
    coords: list[tuple[int, int]] = [cur]

    for i in input:
        d = (i[0][0] * i[1], i[0][1] * i[1])
        cur = (cur[0] + d[0], cur[1] + d[1])
        coords.append(cur)
        # print(cur)

    poly = shapely.Polygon(coords).buffer(0.5, join_style="mitre")
    print(f"Total 2: {int(poly.area)}")

    # Pick's theorem
    poly1 = shapely.Polygon(coords)
    print(f"Total 2_2: {int(poly1.area + poly1.length // 2 +1)}")


if __name__ == "__main__":
    part1()
    part2()
