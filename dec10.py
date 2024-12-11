import itertools
import re
from collections import defaultdict

import numpy as np
from pydantic import BaseModel

# Located all trail starts 0s in map
# for each trail do backtracking to map out location of 9
# (note count 9 positions, not trails)
# Sum all counts.


def find_all_val(lines: list[str], val: str) -> list[tuple[int]]:
    # find all X locations.
    positions = []
    for xcord, line in enumerate(lines):
        positions += [(xcord, y.span()[0]) for y in re.finditer(val, line)]

    return positions


def parse_input(input: str) -> list[str]:
    return input.split("\n")


def get_all_starts(lines: list[str]) -> [tuple[int]]:
    start_positions = find_all_val(lines=lines, val="0")
    return start_positions


def is_valid(lines: list[str], pos: tuple[int], new_pos: tuple[int]) -> bool:
    v1 = lines[pos[0]][pos[1]]
    v2 = lines[new_pos[0]][new_pos[1]]
    ascend = {
        "0": "1",
        "1": "2",
        "2": "3",
        "3": "4",
        "4": "5",
        "5": "6",
        "6": "7",
        "7": "8",
        "8": "9",
    }
    return v2 == ascend[v1]


def move(pos: tuple[int], dir: tuple[int], lines: list[str]) -> tuple[int] | None:
    # check valid.
    new_pos = (pos[0] + dir[0], pos[1] + dir[1])
    if new_pos[0] < 0 or new_pos[1] < 0:
        return None
    try:
        lines[new_pos[0]][new_pos[1]]
        return new_pos
    except IndexError:
        return None


def backtrack(
    lines: list[str], pos: tuple[int], results: list[tuple[int]] = None
) -> list[tuple[int]]:
    if results is None:
        results = []

    if lines[pos[0]][pos[1]] == "9":
        results.append(pos)
        return results

    all_possible_dir = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for dir in all_possible_dir:
        new_pos = move(pos, dir, lines)
        if new_pos is not None and is_valid(lines=lines, pos=pos, new_pos=new_pos):
            results = backtrack(lines, new_pos, results)

    return results


def calc_checksum(num_list: list[int]) -> int:
    checksum = 0
    return checksum


def run_all(input: str) -> list[int]:
    lines = parse_input(input=input)

    checksum = 0
    starts = get_all_starts(lines=lines)
    for start in starts:
        results = backtrack(lines=lines, pos=start, results=[])
        checksum += len(set(results))

    # backtrack()
    # checksum = calc_checksum(num_list=num_list)
    return checksum


import time

t0 = time.time()
input_path = "input/dec10.txt"

with open(input_path) as f:
    input = f.read()


val = run_all(input=input)

print(f"checksum: {val}")

t1 = time.time()
print(f"time: {(t1-t0)} secunds")
