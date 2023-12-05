import sys
from dataclasses import dataclass, field
from itertools import groupby
from pprint import pprint


def read_lines() -> list[str]:
    with open("05/input_example", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


@dataclass
class Range:
    start: int
    range: int
    end: int = field(init=False)

    def __post_init__(self):
        self.end = self.start + self.range


class RangeMapping:
    ranges: list[Range]

    def __init__(self) -> None:
        self.ranges = []

    def add_range(self, range: Range) -> None:
        self.ranges.append(range)


@dataclass
class StaticMapping:
    source: Range
    destination: Range

    def is_in_source_range(self, ranges: list[Range]) -> bool:
        for range in ranges:
            if range.start >= self.source.start and range.end <= self.source.end:
                return True
        return False

    def get_destination_ranges(self, range_mapping: RangeMapping) -> RangeMapping:
        result = RangeMapping()
        for range in range_mapping.ranges:
            # no overlap -> range stays the same -> 1 entry
            if self.source.start >= range.end or self.source.end <= range.start:
                result.add_range(range)
            # fully in source range -> range fully mapped -> 1 entry
            if self.source.start <= range.start and self.source.end >= range.end:
                # get offset and return destination
                offset = range.start - self.source.start
                result.add_range(Range(self.destination.start + offset, range.range))
            # lower start and higher end than source -> 3 entries
            if self.source.start >= range.start and self.source.end <= range.end:
                pass
            # lower start than source -> 2 entries
            if self.source.start >= range.start and self.source.end >= range.end:
                pass
            # higher end than source -> entries
            if self.source.start <= range.start and self.source.end <= range.end:
                pass

        return result


def parse_static_mapping(group: list[str]) -> list[StaticMapping]:
    l: list[StaticMapping] = []
    for x in group[1:]:
        m = [int(s) for s in x.split(" ")]
        dr = Range(start=m[0], range=m[2])
        sr = Range(start=m[1], range=m[2])
        l.append(StaticMapping(source=sr, destination=dr))
    return l


def part2():
    lines = read_lines()
    groups = [list(group) for k, group in groupby(lines, lambda x: x == "") if not k]
    result = sys.maxsize

    for group in groups:
        match group[0]:
            case s if s.startswith("seeds:"):
                seeds = []
                seed_pairs = [int(s) for s in s.split(":")[1].strip().split(" ")]
                for i in range(0, len(seed_pairs), 2):
                    seeds.append(Range(start=seed_pairs[i], range=seed_pairs[i + 1]))
            case "seed-to-soil map:":
                seed_soil = parse_static_mapping(group)
            case "soil-to-fertilizer map:":
                soil_fert = parse_static_mapping(group)
            case "fertilizer-to-water map:":
                fert_water = parse_static_mapping(group)
            case "water-to-light map:":
                water_light = parse_static_mapping(group)
            case "light-to-temperature map:":
                light_temp = parse_static_mapping(group)
            case "temperature-to-humidity map:":
                temp_hum = parse_static_mapping(group)
            case "humidity-to-location map:":
                hum_loc = parse_static_mapping(group)

    for seed in seeds:
        seed_soil.get_destination_ranges(seed, seed_soil)
        # print(f"soil {soil}")
        fert = get_destination_ranges(soil, soil_fert)
        # print(f"fert {fert}")
        water = get_destination_ranges(fert, fert_water)
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

    print(f"Result 2: {result}")


if __name__ == "__main__":
    part2()
