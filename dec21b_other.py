# from https://github.com/gid/AoC/blob/main/src/aoc/2024/day21.py

from collections import deque
from functools import cache

example_input = """029A
980A
179A
456A
379A"""

UP, DOWN, LEFT, RIGHT, ACTIVATE = "^", "v", "<", ">", "A"
NUMERIC_KEYPAD = {
    "0": {UP: "2", RIGHT: "A"},
    "1": {UP: "4", RIGHT: "2"},
    "2": {UP: "5", RIGHT: "3", DOWN: "0", LEFT: "1"},
    "3": {UP: "6", DOWN: "A", LEFT: "2"},
    "4": {UP: "7", RIGHT: "5", DOWN: "1"},
    "5": {UP: "8", RIGHT: "6", DOWN: "2", LEFT: "4"},
    "6": {UP: "9", DOWN: "3", LEFT: "5"},
    "7": {RIGHT: "8", DOWN: "4"},
    "8": {RIGHT: "9", DOWN: "5", LEFT: "7"},
    "9": {DOWN: "6", LEFT: "8"},
    "A": {UP: "3", LEFT: "0"},
}
DIRECTIONAL_KEYPAD = {
    UP: {DOWN: DOWN, RIGHT: ACTIVATE},
    DOWN: {RIGHT: RIGHT, UP: UP, LEFT: LEFT},
    LEFT: {RIGHT: DOWN},
    RIGHT: {UP: ACTIVATE, LEFT: DOWN},
    ACTIVATE: {DOWN: RIGHT, LEFT: UP},
}


def paths(start_key: str, target_key: str, keypad: dict[str, dict[str, str]]) -> str:
    paths, to_visit = [], deque([(start_key, "")])
    while to_visit:
        current_key, sequence = to_visit.popleft()
        if paths and len(sequence) > len(paths[0]):
            break
        if current_key == target_key:
            paths.append(sequence)
        for direction, next_key in keypad[current_key].items():
            if next_key is not None:
                to_visit.append((next_key, sequence + direction))
    return paths


def all_paths(keypad):
    return {(k0, k1): paths(k0, k1, keypad) for k1 in keypad for k0 in keypad}


NUMERIC_PATHS = all_paths(NUMERIC_KEYPAD)
ARROW_PATHS = all_paths(DIRECTIONAL_KEYPAD)

print(ARROW_PATHS)


@cache
def shortest_sequence(instructions, n_robots):
    if n_robots == 0:
        return len(instructions) + 1
    sequence_length = 0
    for from_to in zip("A" + instructions, instructions + ACTIVATE):
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


def solve(inputs: str):
    codes = inputs.splitlines()
    print(f"Part 1: {sum(complexity(code, n_robots=2) for code in codes)}")
    print(f"Part 2: {sum(complexity(code, n_robots=25) for code in codes)}\n")


input_path = "input/dec21.txt"
with open(input_path) as f:
    input = f.read()
actual_input = input

solve(example_input)
solve(actual_input)
