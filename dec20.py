# algo idea
# Run though path once, store all coordinate with timestep
# run though path again. check all possilbe cheats,
# record time saved by comparing to dict with original time


def get_maze_ends(maze: list[str]) -> tuple[tuple[int | tuple[int]]]:
    start = end = None
    for r, row in enumerate(maze):
        for c, char in enumerate(row):
            if char == "S":
                start = (r, c)
            if char == "E":
                end = (r, c)
    return start, end


# Iterate over the linked list and apply splits
def parse_input(input: str) -> list[str]:
    return input.split("\n")


def get_move_dict(maze, start, end) -> dict[tuple[int], int]:
    DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
    cur = start
    step = 0
    moves = {}
    while cur != end:
        moves[cur] = step
        for d in DIRS:
            new = (cur[0] + d[0], cur[1] + d[1])
            if maze[new[0]][new[1]] != "#" and not new in moves:
                cur = new
                step += 1
                print(cur, step, end="\r")
                break
    # remember last step
    moves[cur] = step
    return moves


def count_greater(shortcuts, threshold) -> int:
    count = 0
    for s in shortcuts:
        if s >= threshold:
            count += shortcuts[s]
    return count


def count_shortcuts(moves: dict[tuple[int], int]) -> dict[int, int]:
    DIRS = ((2, 0), (-2, 0), (0, 2), (0, -2))
    shortcuts = {}
    bigshorts = 0
    for m in moves:
        for d in DIRS:
            new = (m[0] + d[0], m[1] + d[1])
            if new in moves:
                move_count = moves[m] + 2
                save = moves[new] - move_count
                if save > 0:
                    if save in shortcuts:
                        shortcuts[save] += 1
                    else:
                        shortcuts[save] = 1
                if save >= 100:
                    bigshorts += 1
    return shortcuts, bigshorts


def run_all(input: str) -> int:
    maze = parse_input(input=input)
    start, end = get_maze_ends(maze=maze)
    moves = get_move_dict(maze=maze, start=start, end=end)
    shortcuts, bigshorts = count_shortcuts(moves=moves)
    # tmp = [(k, v) for k, v in shortcuts.items()]
    # tmp.sort()
    # print(tmp)
    print("~" * 30)
    tmp = [(v, k) for k, v in moves.items()]
    tmp.sort()
    # print(tmp[:10])
    count = count_greater(shortcuts=shortcuts, threshold=100)
    out = count

    return out, bigshorts


import time

t0 = time.time()
input_path = "input/dec20.txt"

with open(input_path) as f:
    input = f.read()


val = run_all(input=input)

print(f"checksum: {val}")

t1 = time.time()
print(f"time: {(t1-t0)} seconds")
