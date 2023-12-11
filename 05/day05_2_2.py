import sys

from itertools import groupby, combinations


class Range:
    end: int
    range: int
    start: int

    def __init__(self, start, range) -> None:
        self.start = start
        self.range = range
        self.end = self.start + self.range

    def __lt__(self, other):
        return self.start < other.start

    def __eq__(self, other):
        return self.start == other.start and self.range == other.range

    def __hash__(self):
        return hash(str(self.start) + str(self.range))


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


def map(inputs: list[Range], mappings: list[Mapping]) -> list[Range]:
    output: list[Range] = []
    tmp: list[Range] = []
    deletes: list[Range] = []
    for mapping in mappings:
        tmp = []
        for input in inputs:
            # no overlap -> range stays the same -> 1 entry
            if mapping.src.start >= input.end or mapping.src.end <= input.start:
                # tmp.append(input)
                pass
            # fully in source range -> range fully mapped -> 1 entry
            if mapping.src.start <= input.start and mapping.src.end >= input.end:
                # get offset and return destination
                offset = input.start - mapping.src.start
                output.append(Range(mapping.dest.start + offset, input.range))
                deletes.append(input)
            # lower start and higher end than source -> 3 entries
            if mapping.src.start >= input.start and mapping.src.end <= input.end:
                # complete desitination
                output.append(Range(mapping.dest.start, mapping.dest.range))
                # below source
                tmp.append(Range(input.start, mapping.src.start - input.start))
                # above source
                tmp.append(Range(mapping.src.end, input.end - mapping.src.end))
                deletes.append(input)
            # lower start than source -> 2 entries
            if mapping.src.start < input.end and mapping.src.start >= input.start and mapping.src.end >= input.end:
                # below source
                tmp.append(Range(input.start, mapping.src.start - input.start))
                # calcaulated destination
                offset = input.end - mapping.src.start
                output.append(Range(mapping.dest.start, offset))
                deletes.append(input)
            # higher end than source -> 2 entries
            if mapping.src.end > input.start and mapping.src.start <= input.start and mapping.src.end <= input.end:
                # above source
                tmp.append(Range(mapping.src.end, input.end - mapping.src.end))
                # calucalated destination
                offset = input.start - mapping.src.start
                output.append(Range(mapping.dest.start + offset, offset))
                deletes.append(input)
            # inputs.remove(input)
        inputs.extend(tmp)
    for d in deletes:
        try:
            inputs.remove(d)
        except ValueError:
            pass

    output.extend(inputs)
    output = deduplicate_ranges(output)
    return output


def read_lines() -> list[str]:
    with open("05/input", "r") as f:
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


def deduplicate_ranges(ranges: list[Range]) -> list[Range]:
    output: list[Range] = ranges.copy()
    for r1, r2 in combinations(ranges, 2):
        if r1.start >= r2.start and r1.end <= r2.end:
            try:
                output.remove(r1)
            except ValueError:
                pass
        if r2.start >= r1.start and r2.end <= r1.end:
            try:
                output.remove(r2)
            except ValueError:
                pass

    return list(set(output))


def part2():
    m = Mappings(group_mappings())
    result = sys.maxsize
    soil = map(m.seeds.copy(), m.mapping_dict["to_soil"])

    # soil = deduplicate_ranges(soil)
    soil.sort()
    for i, s in enumerate(soil):
        if s.start == 41218238:
            print(f"{s.start}, {s.range}, {s.end}")

    print("soil")
    fertilizer = map(soil.copy(), m.mapping_dict["to_fertilizer"])
    print("fert")
    water = map(fertilizer.copy(), m.mapping_dict["to_water"])
    print("water")
    light = map(water.copy(), m.mapping_dict["to_light"])
    print("light")
    temperature = map(light.copy(), m.mapping_dict["to_temperature"])
    print("temp")
    humidity = map(temperature.copy(), m.mapping_dict["to_humidity"])
    print("hum")
    location = map(humidity.copy(), m.mapping_dict["to_location"])
    print("loc")

    for x in location:
        if result > x.start:
            result = x.start

    print(result)


if __name__ == "__main__":
    part2()
