# algo idea
# Brute force / iterative search
# Use dict sorted by first letters to limit search space.
# Possible other hack
import itertools
import re

from cachetools import cached
from cachetools.keys import hashkey

COLORS = ["w", "u", "b", "r", "g"]


# Iterate over the linked list and apply splits
def parse_input(input: str) -> tuple[list[str]]:
    tmp = input.split("\n")
    towels = [i.strip() for i in tmp[0].split(",")]
    combinations = tmp[2:]
    return (towels, combinations)


def sort_towels(*, towels: list[str], n: int) -> dict[str, list[str]]:
    def insert_possible_empty(
        dic: dict[str, list[str]], key: str, val: list[str]
    ) -> dict[str, list[str]]:
        if not key in dic:
            dic[key] = []
        dic[key].append(val)
        return dic

    n_towels = {}
    for towel in towels:
        if len(towel) >= n:
            key = towel[:n]
            n_towels = insert_possible_empty(dic=n_towels, key=key, val=towel)
        else:
            key = towel
            n_towels = insert_possible_empty(dic=n_towels, key=key, val=towel)
            for comb in itertools.permutations(COLORS, n - len(towel)):
                key = towel + "".join(comb)
                n_towels = insert_possible_empty(dic=n_towels, key=key, val=towel)

    return n_towels


def get_regex(towels: list[str]) -> re.Pattern:
    # "any number of any of the patterns, consuming the entire string."
    regex = "^(" + "|".join(towels) + ")+$"
    h = re.compile(regex)
    return h


def regex_match(seq: str, regex_pattern: re.Pattern) -> bool:
    return regex_pattern.match(seq)


def seq_search(
    seq: str, i: int, matched: str, nlist: dict[str, list[dict]], n: int
) -> str:
    """Find the value of register A that will output the specified target"""
    if len(seq) == i:
        return matched
    if len(seq) - i < n:
        n = len(seq) - i
    for ni in range(3, n + 1):
        if seq[i : i + ni] in nlist:
            for candidate in nlist[seq[i : i + ni]]:
                # Extend register A by 3 bits and see if we output the last token in the target
                clen = len(candidate)
                if candidate == seq[i : i + clen]:
                    try:
                        return seq_search(
                            seq=seq,
                            i=i + clen,
                            matched=f"{matched} {candidate}",
                            nlist=nlist,
                            n=n,
                        )
                    except StopIteration:
                        continue
    raise StopIteration


from functools import cache


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

    valid = 0

    clen = len(combis)
    for ci, combi in enumerate(combis):
        print(f"{ci+1}/{clen}", end="\r")
        c = count(t=combi, patterns=towels)
        if c > 0:
            valid += 1

    out = valid
    return out


def run_all3(input: str) -> int:
    towels, combis = parse_input(input=input)
    regex_pattern = get_regex(towels)

    valid = 0
    clen = len(combis)
    for ci, combi in enumerate(combis):
        print(f"{ci+1}/{clen}", end="\r")
        if regex_match(seq=combi, regex_pattern=regex_pattern):
            valid += 1
    print()

    out = valid
    return out


def run_all2(input: str) -> int:
    towels, combis = parse_input(input=input)
    n = 5
    n_towels = sort_towels(towels=towels, n=n)
    print(f"n_towels made for {n}")
    valid = 0
    clen = len(combis)
    for ci, combi in enumerate(combis):
        try:
            seq = seq_search(seq=combi, i=0, matched="", nlist=n_towels, n=n)
            print(f"{ci+1}/{clen}: {combi} - {seq}")
            valid += 1
        except StopIteration:
            print(f"{ci+1}/{clen}: {combi} X NO MATCH")

    out = valid
    return out


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
