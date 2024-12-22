# algo idea
# Brute force / iterative search
# Use dict sorted by first letters to limit search space.
# Possible other hack

# Adapted from
# https://brainwagon.org/2024/12/19/another-chapter-in-the-im-dimwitted-theme-from-advent-of-code-2024/

# from functools import cache

from cachetools import cached
from cachetools.keys import hashkey


# Iterate over the linked list and apply splits
def parse_input(input: str) -> tuple[list[str]]:
    tmp = input.split("\n")
    towels = [i.strip() for i in tmp[0].split(",")]
    combinations = tmp[2:]
    return (towels, combinations)


@cached(cache={}, key=lambda t, **kwargs: hashkey(t))
def count(t: str, patterns: list[str]) -> int:
    cnt = 0
    for p in patterns:
        if t == "":
            return 1
        if t.startswith(p):
            cnt += count(t=t[len(p) :], patterns=patterns)
    return cnt


def run_all(input: str) -> int:
    towels, combis = parse_input(input=input)

    counts = 0

    clen = len(combis)
    for ci, combi in enumerate(combis):
        print(f"{ci+1}/{clen}", end="\r")
        c = count(t=combi, patterns=towels)
        counts += c

    return counts


import time

t0 = time.time()
input_path = "input/dec19.txt"

with open(input_path) as f:
    input = f.read()


val = run_all(input=input)

print(f"checksum: {val}")

t1 = time.time()
print(f"time: {(t1-t0)} seconds")

# 140 - too low
# 140 - too low
# 140 - too low
# 140 - too low
# 140 - too low
# 140 - too low
