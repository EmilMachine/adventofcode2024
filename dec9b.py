import itertools
from collections import defaultdict

import numpy as np
from pydantic import BaseModel

# Preallocate the list
# move one id at a time
# iterate over blocks from behind
# Try to move from left.
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


def update_start(start: int, num_list: list[int]) -> int:
    while num_list[start] is not None:
        start += 1
    return start


def update_end(end: int, num_list: list[int]) -> int:
    while num_list[end] is None:
        end -= 1
    return end


def get_endblock(end: int, num_list: list[int]) -> tuple[int]:
    end_start = end
    while num_list[end] == num_list[end_start]:
        end_start -= 1
    return (end_start + 1, end + 1)


def get_startblock(start: int, num_list: list[int], gaplen: int) -> tuple[int] | None:
    start0 = start
    while start0 < len(num_list) - 1 - gaplen:
        if num_list[start0] is None:
            if num_list[start0 : start0 + gaplen] == [None] * gaplen:
                return (start0, start0 + gaplen)
            # else:
            #     start0 += gaplen - 1
        start0 += 1

    return None


def realocate(num_list: list[int]) -> list[int]:
    start = 0
    end = len(num_list) - 1
    max_start_block = len(num_list)
    start = update_start(start=start, num_list=num_list)
    end = update_end(end=end, num_list=num_list)
    while end > start:
        endblock = get_endblock(end=end, num_list=num_list)
        len_end = endblock[1] - endblock[0]

        if max_start_block < len_end:
            startblock = None
        else:
            startblock = get_startblock(start=start, num_list=num_list, gaplen=len_end)
        # only move backward (never forward)
        if startblock is None:
            max_start_block = min(len_end - 1, max_start_block)
        elif startblock[0] > endblock[0]:
            pass
        else:
            # move if we have a start block
            num_list[startblock[0] : startblock[1]] = num_list[
                endblock[0] : endblock[1]
            ]
            num_list[endblock[0] : endblock[1]] = [None] * len_end
        end = endblock[0] - 1
        start = update_start(start=start, num_list=num_list)
        end = update_end(end=end, num_list=num_list)
    return num_list


def calc_checksum(num_list: list[int]) -> int:
    checksum = 0

    for idx, i in enumerate(num_list):
        if i is None:
            continue
        checksum += idx * i
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
