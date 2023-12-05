import sys
from dataclasses import dataclass, field
from itertools import groupby, count
from pprint import pprint


@dataclass
class Mapping:
    d_start: int
    d_end: int = field(init=False)
    s_start: int
    s_end: int = field(init=False)
    range: int

    def __post_init__(self):
        self.d_end = self.d_start + self.range
        self.s_end = self.s_start + self.range

    def is_in_source_range(self, n: int):
        return n >= self.s_start and n < self.s_end

    def is_in_destination_range(self, n: int):
        return n >= self.d_start and n < self.d_end

    def get_mapping(self, n: int):
        if n >= self.s_start and n < self.s_end:
            idx = n - self.s_start
            return self.d_start + idx
        else:
            return n

    def get_reverse_mapping(self, n: int):
        if n >= self.d_start and n < self.d_end:
            idx = n - self.d_start
            return self.s_start + idx
        else:
            return n


def read_lines() -> list[str]:
    with open("05/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def parse_mapping(group: list[str]) -> list[Mapping]:
    l: list[Mapping] = []
    for x in group[1:]:
        m = [int(s) for s in x.split(" ")]
        l.append(Mapping(d_start=m[0], s_start=m[1], range=m[2]))
    return l


def get_mapping(n: int, mappings: list[Mapping]):
    for mapping in mappings:
        if mapping.is_in_source_range(n):
            return mapping.get_mapping(n)
    return n


def get_reverse_mapping(n: int, mappings: list[Mapping]):
    for mapping in mappings:
        if mapping.is_in_destination_range(n):
            return mapping.get_reverse_mapping(n)
    return n


def part1():
    lines = read_lines()
    groups = [list(group) for k, group in groupby(lines, lambda x: x == "") if not k]
    result = sys.maxsize

    for group in groups:
        match group[0]:
            case s if s.startswith("seeds:"):
                seeds = [int(s) for s in s.split(":")[1].strip().split(" ")]
            case "seed-to-soil map:":
                seed_soil = parse_mapping(group)
            case "soil-to-fertilizer map:":
                soil_fert = parse_mapping(group)
            case "fertilizer-to-water map:":
                fert_water = parse_mapping(group)
            case "water-to-light map:":
                water_light = parse_mapping(group)
            case "light-to-temperature map:":
                light_temp = parse_mapping(group)
            case "temperature-to-humidity map:":
                temp_hum = parse_mapping(group)
            case "humidity-to-location map:":
                hum_loc = parse_mapping(group)

    for seed in seeds:
        soil = get_mapping(seed, seed_soil)
        # print(f"soil {soil}")
        fert = get_mapping(soil, soil_fert)
        # print(f"fert {fert}")
        water = get_mapping(fert, fert_water)
        # print(f"water {water}")
        light = get_mapping(water, water_light)
        # print(f"light {light}")
        temp = get_mapping(light, light_temp)
        # print(f"temp {temp}")
        hum = get_mapping(temp, temp_hum)
        # print(f"hum {hum}")
        loc = get_mapping(hum, hum_loc)
        # print(f"loc {loc}")
        if result > loc:
            result = loc

    print(f"Result 1: {result}")


def part2():
    lines = read_lines()
    groups = [list(group) for k, group in groupby(lines, lambda x: x == "") if not k]
    result = 0

    for group in groups:
        match group[0]:
            case s if s.startswith("seeds:"):
                seeds = []
                seed_pairs = [int(s) for s in s.split(":")[1].strip().split(" ")]
                for i in range(0, len(seed_pairs), 2):
                    seeds.append((seed_pairs[i], seed_pairs[i] + seed_pairs[i + 1]))
            case "seed-to-soil map:":
                seed_soil = parse_mapping(group)
            case "soil-to-fertilizer map:":
                soil_fert = parse_mapping(group)
            case "fertilizer-to-water map:":
                fert_water = parse_mapping(group)
            case "water-to-light map:":
                water_light = parse_mapping(group)
            case "light-to-temperature map:":
                light_temp = parse_mapping(group)
            case "temperature-to-humidity map:":
                temp_hum = parse_mapping(group)
            case "humidity-to-location map:":
                hum_loc = parse_mapping(group)

    for location in count():
        # print(f"loc {location}")
        hum = get_reverse_mapping(location, hum_loc)
        # print(f"hum {hum}")
        temp = get_reverse_mapping(hum, temp_hum)
        # print(f"temp {temp}")
        light = get_reverse_mapping(temp, light_temp)
        # print(f"light {light}")
        water = get_reverse_mapping(light, water_light)
        # print(f"water {water}")
        fert = get_reverse_mapping(water, fert_water)
        # print(f"fert {fert}")
        soil = get_reverse_mapping(fert, soil_fert)
        # print(f"soil {soil}")
        seed = get_reverse_mapping(soil, seed_soil)
        # print(f"seed {seed}")
        for s in seeds:
            if seed >= s[0] and seed <= s[1]:
                return location
        if location % 1000000 == 0:
            print(location)


if __name__ == "__main__":
    part1()
    # This will take a while...
    print(f"Result 2: {part2()}")
