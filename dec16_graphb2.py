# algo idea
# Read map
# Spawn raindeers at any intersection
# (never let raindeer backtrack) (revisit location)
# retrun the raindeer with the lowest score
### DO THE FUCKING GRAPH AS 4 DIRECTIONED GRAPHS WHERE MOVING BETWEEN THEM (IE ROTATING COST 1000)


import networkx as nx

ROTATION_COST = 1000
MOVE_COST = 1
# Directions and corresponding movements
DIRECTIONS = {
    "E": (0, 1),  # East
    "W": (0, -1),  # West
    "N": (-1, 0),  # North
    "S": (1, 0),  # South
}

DIRECTION_TURNS = {
    "E": ("N", "S"),  # East
    "W": ("N", "S"),  # West
    "N": ("E", "W"),  # North
    "S": ("E", "W"),  # South
}


def get_maze_ends(maze: list[str]) -> tuple[tuple[int | tuple[int]]]:
    start = end = None
    for r, row in enumerate(maze):
        for c, char in enumerate(row):
            if char == "S":
                start = (r, c, "E")  # Start facing East
            if char == "E":
                end = (r, c)
    return start, end


def is_wall(maze: list[str], r: int, c: int):
    return maze[r][c] == "#"


def build_graph(maze: list[str], start: tuple[int | str]):
    G = nx.DiGraph()
    rows, cols = len(maze), len(maze[0])
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if not is_wall(maze, r, c):
                # for each Direction
                for dir in DIRECTIONS:
                    # add moves to other direction.
                    for new_dir in DIRECTION_TURNS[dir]:
                        G.add_edge((r, c, dir), (r, c, new_dir), weight=ROTATION_COST)
                    # check move within direction.
                    dr, dc = DIRECTIONS[dir]
                    if not is_wall(maze, r + dr, c + dc):
                        G.add_edge((r, c, dir), (r + dr, c + dc, dir), weight=MOVE_COST)

    return G


def find_shortest_path(G: nx.Graph, start: tuple[int | str], end: tuple[int]):
    try:
        min_length = float("inf")
        min_path = []
        # test all end directions
        for d in DIRECTIONS:
            length, path = nx.single_source_dijkstra(G, start, (end[0], end[1], d))
            if length < min_length:
                min_length = length
                min_path = path

        return min_length, min_path
    except nx.NetworkXNoPath:
        return float("inf"), []


def calculate_distance(path, graph):
    distance = 0
    for i in range(len(path) - 1):
        distance += graph[path[i]][path[i + 1]]["weight"]
    return distance


def find_shortest_paths(
    G: nx.Graph, start: tuple[int | str], end: tuple[int | str]
) -> list[list[tuple[int | str]]]:
    try:
        min_length = float("inf")
        min_paths = []
        # test all end directions
        for d in DIRECTIONS:
            paths = list(
                nx.all_shortest_paths(
                    G, source=start, target=(end[0], end[1], d), weight="weight"
                )
            )
            length = calculate_distance(path=paths[0], graph=G)
            if length < min_length:
                min_length = length
                min_paths = paths
            elif length == min_length:
                min_paths += paths

        return min_paths
    except nx.NetworkXNoPath:
        return []


# Iterate over the linked list and apply splits
def parse_input(input: str) -> list[str]:
    return input.split("\n")


def combine_path_length(paths: list[tuple[int]]) -> int:
    places = []
    for path in paths:
        places += [p[:2] for p in path]
    return len(set(places))


def run_all(input: str) -> int:
    maze = parse_input(input=input)
    for line in maze:
        print(line)

    start, end = get_maze_ends(maze=maze)
    G = build_graph(maze, start=start)
    print("build graph")

    # checksum = find_shortest_path(G=G, start=start, end=end)
    paths = find_shortest_paths(G, start, end)
    print(f"n paths: {len(paths)}")
    checksum = combine_path_length(paths)
    return checksum


import time

t0 = time.time()
input_path = "input/dec16.txt"
# extra test cases from
# https://www.reddit.com/r/adventofcode/comments/1hfhgl1/2024_day_16_part_1_alternate_test_case/

with open(input_path) as f:
    input = f.read()


val = run_all(input=input)

print(f"checksum: {val}")

t1 = time.time()
print(f"time: {(t1-t0)} seconds")


# test3
# Part 1: 21148
# Part 2: 149

# test4
# Part 1: 5078
# Part 2: 413
