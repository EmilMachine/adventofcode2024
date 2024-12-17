# algo idea
# Read map
# Spawn raindeers at any intersection
# (never let raindeer backtrack) (revisit location)
# retrun the raindeer with the lowest score

import copy
from collections import deque

import networkx as nx

# Sample maze input
# Constanct
rotation_cost = 1001
move_cost = 1


def get_maze_ends(maze: list[str]) -> tuple[tuple[int | tuple[int]]]:
    start = end = None
    for r, row in enumerate(maze):
        for c, char in enumerate(row):
            if char == "S":
                start = (r, c, (0, 1))  # Start facing East
            if char == "E":
                end = (r, c)
    return start, end


def is_wall(r, c, maze):
    return maze[r][c] == "#"


def build_graph(maze, start):
    G = nx.Graph()
    tocheck = deque([start])
    visited = set()

    while tocheck:
        r, c, direction = tocheck.popleft()
        dr, dc = direction

        # check the neighbors - with correct cost
        possible_dir = (
            (dr, dc, move_cost),
            (dc, -1 * dr, rotation_cost),
            (-1 * dc, dr, rotation_cost),
        )
        for pdr, pdc, cost in possible_dir:
            nr, nc = r + pdr, c + pdc
            if not is_wall(r=nr, c=nc, maze=maze):
                # If alreay in graph just add a link
                if (nr, nc) in visited:
                    G.add_edge((r, c), (nr, nc), weight=rotation_cost)
                else:
                    G.add_node((nr, nc))
                    G.add_edge((r, c), (nr, nc), weight=cost)
                    visited.add((nr, nc))
                    if (dr, dc) == (pdr, pdc):
                        # explore straight first
                        tocheck.appendleft((nr, nc, (pdr, pdc)))
                    else:
                        tocheck.append((nr, nc, (pdr, pdc)))

    return G


def find_shortest_paths(G, start, end):
    try:
        paths = list(
            nx.all_shortest_paths(G, source=start, target=end, weight="weight")
        )
        return paths
    except nx.NetworkXNoPath:
        return []


# Iterate over the linked list and apply splits
def parse_input(input: str) -> list[str]:
    return input.split("\n")


import matplotlib.pyplot as plt


def plot_graph(G):
    pos = {node: node for node in G.nodes()}

    # Define a color map based on edge weights
    edge_colors = []
    for u, v, data in G.edges(data=True):
        weight = data["weight"]
        if weight == 1:
            edge_colors.append("green")
        else:
            edge_colors.append("red")

    # Draw the graph
    plt.figure(figsize=(8, 6))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=700,
        node_color="lightblue",
        font_size=10,
        font_color="black",
    )
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2)
    plt.title("Graph with Different Edge Weights")
    plt.show()


def plot_explored(maze: list[str], path: list[tuple[int]]) -> None:
    tmp_plan = [list(line) for line in maze]

    for count, step in enumerate(path):
        tmp_plan[step[0]][step[1]] = str(count % 10)
    for line in tmp_plan:
        print("".join(line))


def recount_path(path: list[tuple[int]]) -> int:
    dir = (0, 1)  # start east
    pos = path[0]
    cost = 0
    for p in path[1:]:
        new_dir = (p[0] - pos[0], p[1] - pos[1])
        if dir != new_dir:
            cost += 1001
        else:
            cost += 1
        dir = new_dir
        pos = p
    return cost


def is_diagonal(node1, node2):
    return abs(node1[0] - node2[0]) == 1 and abs(node1[1] - node2[1]) == 1


def modify_graph(G):
    nodes_to_remove = [node for node in G.nodes() if 3 <= G.degree[node] <= 4]
    for node in nodes_to_remove:
        neighbors = list(G.neighbors(node))
        # Remove the node
        G.remove_node(node)
        # Connect neighbors
        for i, n1 in enumerate(neighbors):
            for j, n2 in enumerate(neighbors):
                if i < j:
                    new_node = (node[0], node[1], i, j)
                    if is_diagonal(n1, n2):
                        G.add_node(new_node)
                        G.add_edge(n1, new_node, weight=1)
                        G.add_edge(new_node, n2, weight=1001)

                    else:
                        G.add_node(new_node)
                        G.add_edge(n1, new_node, weight=1)
                        G.add_edge(new_node, n2, weight=1)


def combine_path_length(paths: list[tuple[int]]) -> int:
    places = []
    for path in paths:
        places += [p[:2] for p in path]
    return len(set(places))


def run_all(input: str) -> int:
    maze = parse_input(input=input)
    start_with_dir, end = get_maze_ends(maze=maze)
    start = start_with_dir[:2]
    G = build_graph(maze, start=start_with_dir)
    print("build graph")
    modify_graph(G)
    print("modified graph")
    paths = find_shortest_paths(G, start, end)
    print(len(paths), recount_path(path=paths[0]))
    # for p in paths:
    #     print(p)

    checksum = combine_path_length(paths)
    return checksum


import time

t0 = time.time()
input_path = "input/dec16_test4.txt"
# extra test cases from
# https://www.reddit.com/r/adventofcode/comments/1hfhgl1/2024_day_16_part_1_alternate_test_case/

with open(input_path) as f:
    input = f.read()


val = run_all(input=input)

print(f"safety number: {val}")

t1 = time.time()
print(f"time: {(t1-t0)} seconds")

# 545 too low
