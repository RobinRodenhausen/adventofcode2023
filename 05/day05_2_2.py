import sys

from itertools import groupby


class Range:
    end: int
    range: int
    start: int

    def __init__(self, start, range) -> None:
        self.start = start
        self.range = range
        self.end = self.start + self.range


class Mapping:
    dest: Range
    src: Range

    def __init__(self, dest_start: int, src_start: int, range: int) -> None:
        self.dest = Range(dest_start, range)
        self.src = Range(src_start, range)


class Mappings:
    def __init__(self, groups: list[list[str]]) -> None:
        self.seeds: list[Range] = []
        self.mapping_dict = {
            "to_soil": [],
            "to_fertilizer": [],
            "to_water": [],
            "to_light": [],
            "to_temperature": [],
            "to_humidity": [],
            "to_location": [],
        }

        for group in groups:
            match group[0]:
                case s if s.startswith("seeds:"):
                    seed_pairs = [int(s) for s in s.split(":")[1].strip().split(" ")]
                    for i in range(0, len(seed_pairs), 2):
                        self.seeds.append(Range(start=seed_pairs[i], range=seed_pairs[i + 1]))
                case "seed-to-soil map:":
                    self.mapping_dict["to_soil"].extend(group_to_mapping(group))
                case "soil-to-fertilizer map:":
                    self.mapping_dict["to_fertilizer"].extend(group_to_mapping(group))
                case "fertilizer-to-water map:":
                    self.mapping_dict["to_water"].extend(group_to_mapping(group))
                case "water-to-light map:":
                    self.mapping_dict["to_light"].extend(group_to_mapping(group))
                case "light-to-temperature map:":
                    self.mapping_dict["to_temperature"].extend(group_to_mapping(group))
                case "temperature-to-humidity map:":
                    self.mapping_dict["to_humidity"].extend(group_to_mapping(group))
                case "humidity-to-location map:":
                    self.mapping_dict["to_location"].extend(group_to_mapping(group))


def map_individual(input: Range, mappings: list[Mapping]) -> list[tuple[Mapping, Range]]:
    l: list[tuple[Mapping, Range]] = []
    x = input
    for mapping in mappings:
        # no overlap -> range stays the same -> 1 entry
        if mapping.src.start >= x.end or mapping.src.end <= x.start:
            l.append((mapping, x))
            continue
        # fully in source range -> range fully mapped -> 1 entry
        if mapping.src.start <= x.start and mapping.src.end >= x.end:
            # get offset and return destination
            offset = x.start - mapping.src.start
            l.append((mapping, Range(mapping.dest.start + offset, x.range)))
            continue
        # lower start and higher end than source -> 3 entries
        if mapping.src.start >= x.start and mapping.src.end <= x.end:
            # complete desitination
            l.append((mapping, Range(mapping.dest.start, mapping.dest.range)))
            # below source
            l.append((mapping, Range(x.start, mapping.src.start - x.start)))
            # above source
            l.append((mapping, Range(mapping.src.end, x.end - mapping.src.end)))
            continue
        # lower start than source -> 2 entries
        if mapping.src.start < x.end and mapping.src.start >= x.start and mapping.src.end >= x.end:
            # below source
            l.append((mapping, Range(x.start, mapping.src.start - x.start)))
            # calcaulated destination
            offset = x.end - mapping.src.start
            l.append((mapping, Range(mapping.dest.start, offset)))
            continue
        # higher end than source -> 2 entries
        if mapping.src.end > x.start and mapping.src.start <= x.start and mapping.src.end <= x.end:
            # above source
            l.append((mapping, Range(mapping.src.end, x.end - mapping.src.end)))
            # calucalated destination
            offset = x.start - mapping.src.start
            l.append((mapping, Range(mapping.dest.start + offset, offset)))
            continue
    return l


def map(input: list[Range], mappings: list[Mapping]) -> list[Range]:
    tmp: list[tuple[Mapping, Range]] = []

    for i in input:
        tmp.extend(map_individual(i, mappings))

    return []


def read_lines() -> list[str]:
    with open("05/input_example", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def group_mappings() -> list[list[str]]:
    lines = read_lines()
    return [list(group) for k, group in groupby(lines, lambda x: x == "") if not k]


def group_to_mapping(group: list[str]) -> list[Mapping]:
    l: list[Mapping] = []
    for x in group[1:]:
        m = [int(s) for s in x.split(" ")]
        l.append(Mapping(dest_start=m[0], src_start=m[1], range=m[2]))
    return l


def part2():
    m = Mappings(group_mappings())
    result = sys.maxsize
    soil = []
    soil.extend(map(m.seeds, m.mapping_dict["to_soil"]))
    fertilizer = []
    for x in m.mapping_dict["to_fertilizer"]:
        fertilizer.extend(map(soil, x))
    water = []
    for x in m.mapping_dict["to_water"]:
        water.extend(map(fertilizer, x))
    light = []
    for x in m.mapping_dict["to_light"]:
        light.extend(map(water, x))
    temperature = []
    for x in m.mapping_dict["to_temperature"]:
        temperature.extend(map(light, x))
    humidity = []
    for x in m.mapping_dict["to_humidity"]:
        humidity.extend(map(temperature, x))
    location: list[Range] = []
    for x in m.mapping_dict["to_location"]:
        location.extend(map(humidity, x))

    for x in location:
        if result > x.start:
            result = x.start

    print(result)


if __name__ == "__main__":
    part2()
