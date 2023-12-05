from itertools import groupby, count

seeds: list[tuple[int,int,int]] = []

def parse_file():
    with open("05/input_example", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

    groups = [list(group) for k, group in groupby(lines, lambda x: x == "") if not k]

    for group in groups:
        print(group)
        if group[0].startswith("seeds:")


# def group_to_mapping(group: list[str]) -> list[Mapping]:
#     l: list[Mapping] = []
#     for x in group[1:]:
#         m = [int(s) for s in x.split(" ")]
#         l.append(Mapping(dest_start=m[0], src_start=m[1], range=m[2]))
#     return l


if __name__ == "__main__":
    parse_file()
