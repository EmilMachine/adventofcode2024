# Implemnet dictonary to keep track of stone, and next type of iteration of stone.
# Implement update of dictionary
import numpy as np


def split_int(a: int) -> tuple[int, int]:
    length = np.ceil(np.log10(a + 1))
    zeros = 10 ** (length / 2)
    left = a // zeros
    right = a - zeros * left
    return int(left), int(right)


def mutate(val: int) -> tuple[int]:
    if val == 0:
        return (1,)
    length = np.ceil(np.log10(val + 1)) % 2 == 0
    if length:
        return split_int(a=val)
    return (val * 2024,)


from collections import defaultdict


def update_dicts(
    count_dict: dict[int, int], evolve_dict: dict[int, tuple[int]]
) -> tuple[dict[int, int] | dict[int, tuple[int]]]:
    new_count = defaultdict(int)
    for stonetype in count_dict:
        if not stonetype in evolve_dict:
            evolve_dict[stonetype] = mutate(stonetype)
        for i in evolve_dict[stonetype]:
            new_count[i] = new_count[i] + count_dict[stonetype]
    return new_count, evolve_dict


# Iterate over the linked list and apply splits
def parse_input(input: str) -> dict[int, int]:
    new_count = defaultdict(int)
    for i in input.split(" "):
        new_count[int(i)] = new_count[int(i)] + 1
    return new_count


def get_sum(count_dict: dict[int, int]) -> int:
    all = 0
    for i in count_dict:
        all += count_dict[i]
    return all


def run_all(input: str, n_blinks=75) -> list[int]:
    count_dict = parse_input(input=input)
    evolve_dict = {}
    t0 = time.time()
    for blink in range(n_blinks):
        t1p = time.time()
        count_dict, evolve_dict = update_dicts(
            count_dict=count_dict, evolve_dict=evolve_dict
        )
        t1 = time.time()
        print(blink, t1 - t0, t1 - t1p)
    return get_sum(count_dict=count_dict)


import time

t0 = time.time()
input_path = "input/dec11.txt"

with open(input_path) as f:
    input = f.read()


val = run_all(input=input, n_blinks=75)

print(f"n stones: {val}")

t1 = time.time()
print(f"time: {(t1-t0)} secunds")
