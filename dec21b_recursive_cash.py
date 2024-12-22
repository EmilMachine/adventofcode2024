# algo idea
# make some dicts that map all from X->Y combination
# For each layer
# Apply translation each level up.
# Calc final checksums
## Instead of applying it keep track of the pairwise combinations
## at the end sum them together with cost

from collections import defaultdict
from functools import cache

# from cachetools import cached
# from cachetools.keys import hashkey


# row, col
NUM_KEYBOARD = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}

# row, col
ARROW_KEYBOARD = {"^": (0, 1), "A": (0, 2), "<": (1, 0), "v": (1, 1), ">": (1, 2)}


def get_paths(v1, v2, forbidden):
    dr = v2[0] - v1[0]
    dc = v2[1] - v1[1]
    if dr > 0:
        rsign = "v"
    else:
        rsign = "^"
    if dc > 0:
        csign = ">"
    else:
        csign = "<"
    dr = abs(dr)
    dc = abs(dc)

    # return row first , colfirst options
    options = (dr * rsign + dc * csign, dc * csign + dr * rsign)
    if options[0] == options[1]:
        options = (options[0],)
    elif (v1[0], v2[1]) == forbidden:
        # colfirst
        options = (options[0],)
    elif (v2[0], v1[1]) == forbidden:
        # rowfirst
        options = (options[1],)

    return options


def get_numeric_paths():
    converter = {}
    forbidden = (3, 0)
    for n1, v1 in NUM_KEYBOARD.items():
        for n2, v2 in NUM_KEYBOARD.items():
            converter[(n1, n2)] = get_paths(v1=v1, v2=v2, forbidden=forbidden)
    return converter


def get_arrow_paths():
    converter = {}
    forbidden = (0, 0)
    for n1, v1 in ARROW_KEYBOARD.items():
        for n2, v2 in ARROW_KEYBOARD.items():
            converter[(n1, n2)] = get_paths(v1=v1, v2=v2, forbidden=forbidden)
    return converter


ARROW_PATHS = get_arrow_paths()
NUMERIC_PATHS = get_numeric_paths()


# Iterate over the linked list and apply splits
def parse_input(input: str) -> dict[str, int]:
    out = {}
    for s in input.split("\n"):
        out[s] = int(s[:-1])
    return out


# @cached(cache={}, key=lambda instructions, **kwargs: hashkey(instructions))
@cache
def shortest_sequence(instructions, n_robots):
    if n_robots == 0:
        # why is it len(instructions) +1
        # because they all miss the finish A press
        return len(instructions) + 1
    sequence_length = 0
    for from_to in zip("A" + instructions, instructions + "A"):
        sequence_length += min(
            shortest_sequence(path, n_robots - 1) for path in ARROW_PATHS[from_to]
        )

    return sequence_length


def complexity(code, n_robots):
    sequence_length = 0
    for from_to in zip("A" + code[:-1], code):
        sequence_length += min(
            shortest_sequence(path, n_robots) for path in NUMERIC_PATHS[from_to]
        )
    return sequence_length * int(code[:-1])


def run_all(input: str) -> int:
    codes = parse_input(input)

    print(f"Part 1: {sum(complexity(code, n_robots=2) for code in codes)}")

    out = 0
    for code in codes:
        out += complexity(code=code, n_robots=25)

    return out


import time

t0 = time.time()
input_path = "input/dec21.txt"

with open(input_path) as f:
    input = f.read()

val = run_all(input=input)
print(f"checksum: {val}")
t1 = time.time()
print(f"time: {(t1-t0)} seconds")

# -----
# 279638326609472

# 851279259176208
