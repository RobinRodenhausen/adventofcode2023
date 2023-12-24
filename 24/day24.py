import itertools
import z3


class Hailstorm:
    px: int
    py: int
    pz: int
    vx: int
    vy: int
    vz: int
    slope: float
    intercept: float

    def __init__(self, line: str) -> None:
        p, v = line.split("@")
        self.px, self.py, self.pz = [int(s) for s in p.split(",")]
        self.vx, self.vy, self.vz = [int(s) for s in v.split(",")]
        # y=ax+b
        # Steigung/slope a = y/x (b is irrelevant for this)
        self.slope = self.vy / self.vx
        # Schnittpunkt/intercept b = y-ax
        self.intercept = self.py - self.slope * self.px


def read_lines() -> list[str]:
    with open("24/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def parse_input() -> list[Hailstorm]:
    lines = read_lines()
    hailstorms: list[Hailstorm] = []
    for line in lines:
        hailstorms.append(Hailstorm(line))
    return hailstorms


def part1():
    # test_low = 7
    # test_high = 27
    test_low = 200000000000000
    test_high = 400000000000000
    hailstorms = parse_input()
    total = 0

    hail1: Hailstorm
    hail2: Hailstorm
    for hail1, hail2 in itertools.combinations(hailstorms, 2):
        # y=ax + b
        # y=cx + d
        # ax + b = cx + d
        # ax - cy = d - b
        # x(a-c) = d-b
        # x = (d-b) / (a-c)

        # parallel (divide by zero)
        if hail1.slope == hail2.slope:
            continue

        x = (hail2.intercept - hail1.intercept) / (hail1.slope - hail2.slope)
        y = hail1.slope * x + hail1.intercept

        # future
        hail1_time = (x - hail1.px) / hail1.vx
        hail2_time = (x - hail2.px) / hail2.vx
        if hail1_time < 0 or hail2_time < 0:
            continue

        if test_low <= x <= test_high and test_low <= y <= test_high:
            total += 1

    print(f"Total 1: {total}")


def part2():
    hailstorms = parse_input()
    px_real, py_real, pz_real, vx_real, vy_real, vz_real = z3.Reals("px_real, py_real, pz_real, vx_real, vy_real, vz_real")
    z3_solver = z3.Solver()

    for hi, hailstorm in enumerate(hailstorms[:3]):
        ti = z3.Real(f"t{hi}")
        z3_solver.add(ti > 0)
        z3_solver.add(px_real + ti * vx_real == hailstorm.px + ti * hailstorm.vx)
        z3_solver.add(py_real + ti * vy_real == hailstorm.py + ti * hailstorm.vy)
        z3_solver.add(pz_real + ti * vz_real == hailstorm.pz + ti * hailstorm.vz)
    z3_solver.check()
    total = sum(z3_solver.model()[var].as_long() for var in [px_real, py_real, pz_real])
    print(f"Total 2: {total}")


if __name__ == "__main__":
    part1()
    part2()
