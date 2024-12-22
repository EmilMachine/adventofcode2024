# algo idea
# Read coordinates
# Make a fully connected graph
# Remove coordinates
# Do shortest path search
# Progressively remove nodes until no path is found
# If not work try to do binary search of when it exactly happens
# Took 20 seconds. it was ok.
import networkx as nx

# Directions and corresponding movements
DIRECTIONS = {
    "E": (0, 1),  # East
    "W": (0, -1),  # West
    "N": (-1, 0),  # North
    "S": (1, 0),  # South
}


def is_in_bound(new_r, new_c, size):
    # only works because size is one smaller than actual size
    # we start from 0
    return new_r >= 0 and new_r <= size and new_c >= 0 and new_c <= size


def build_graph(size: int) -> nx.Graph:
    G = nx.DiGraph()
    # build fully connected graph
    for r in range(0, size + 1):
        for c in range(0, size + 1):
            for dir in DIRECTIONS:
                dr, dc = DIRECTIONS[dir]
                new_r, new_c = r + dr, c + dc
                if is_in_bound(new_r, new_c, size):
                    G.add_edge((r, c), (new_r, new_c), weight=1)

    return G


def remove_notes(G: nx.Graph, nodes: list[tuple[int]]):
    for node in nodes:
        G.remove_node(node)


def find_shortest_path(G: nx.Graph, start: tuple[int], end: tuple[int]):
    try:
        length, path = nx.single_source_dijkstra(G, start, end)
        return length, path
    except nx.NetworkXNoPath:
        return float("inf"), []


# Iterate over the linked list and apply splits
def parse_input(input: str) -> list[tuple[int]]:
    blocks = []
    for line in input.split("\n"):
        blocks.append(tuple(map(int, line.split(","))))
    return blocks


def run_all(input: str) -> int:
    blocks = parse_input(input=input)
    size = max(list(sum(blocks, ())))
    G = build_graph(size=size)
    start = (0, 0)
    end = (size, size)
    for i, block in enumerate(blocks):
        print(i, end="\r")
        remove_notes(G, nodes=[block])
        length, _ = find_shortest_path(G, start, end)
        if length == float("inf"):
            print(i)
            out = block
            break

    return out


import time

t0 = time.time()
input_path = "input/dec18.txt"

with open(input_path) as f:
    input = f.read()


val = run_all(input=input)

print(f"checksum: {val}")

t1 = time.time()
print(f"time: {(t1-t0)} seconds")
