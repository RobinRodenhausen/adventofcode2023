import itertools
import networkx


def read_lines() -> list[str]:
    with open("25/input", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def parse_input() -> networkx.Graph:
    lines = read_lines()

    graph = networkx.Graph()

    for line in lines:
        source, targets = line.split(":")
        for target in targets.split():
            graph.add_edge(source, target, capacity=1)

    return graph


def part1():
    graph = parse_input()
    for s, t in itertools.combinations(list(graph.nodes), 2):
        n, graphs = networkx.minimum_cut(graph, s, t)
        if n == 3:
            print(f"Total 1: {len(graphs[0]) * len(graphs[1])}")
            break


if __name__ == "__main__":
    part1()
