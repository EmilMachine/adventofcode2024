import itertools
from collections import defaultdict

import numpy as np
from pydantic import BaseModel

# Preallocate the list
# move one id at a time
# calc checksum


def parse_input(input: str) -> list[int]:
    num_list = [int(i) for i in list(input)]
    n_elements = sum(num_list)
    out = [None] * n_elements
    pos = 0
    for idx, element in enumerate(num_list):
        if idx % 2 == 0:
            out[pos : pos + element] = [idx // 2] * element
        pos += element
    return out


def update_start(start: int, num_list: list[int]):
    while num_list[start] is not None:
        start += 1
    return start


def update_end(end: int, num_list: list[int]):
    while num_list[end] is None:
        end -= 1
    return end


def realocate(num_list: list[int]) -> list[int]:
    start = 0
    end = len(num_list) - 1
    start = update_start(start=start, num_list=num_list)
    end = update_end(end=end, num_list=num_list)
    while end > start:
        num_list[start] = num_list[end]
        num_list[end] = None
        start = update_start(start=start, num_list=num_list)
        end = update_end(end=end, num_list=num_list)
    return num_list


def calc_checksum(num_list: list[int]) -> int:
    checksum = 0
    i = 0
    while num_list[i] is not None:
        checksum += i * num_list[i]
        i += 1
    return checksum


def run_all(input: str) -> list[int]:
    num_list = parse_input(input)
    num_list = realocate(num_list)
    checksum = calc_checksum(num_list=num_list)
    return checksum


import time

t0 = time.time()
input_path = "input/dec9.txt"

with open(input_path) as f:
    input = f.read()


val = run_all(input=input)
print(f"checksum: {val}")

t1 = time.time()
print(f"time: {(t1-t0)} secunds")
