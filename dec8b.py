import itertools
from collections import defaultdict

import numpy as np
from pydantic import BaseModel

# algo parse input and put all antennae of same type in dict (with coordinates)
# for each attenae type, create all 2 attenaeu permutation
# calculate antinote positions and add to collection
# remove duplicate antinotes, and antinotes out of bounds.


class Antennamap(BaseModel):
    map: list[list[str]] = []
    xmax: int = 0
    ymax: int = 0
    antennae: dict[str, list[list[int]]] = {}


def locate_antennae(citymap: list[list[str]]) -> dict[str, list[list[int]]]:
    antennae = defaultdict(list)
    for idx, line in enumerate(citymap):
        for idy, char in enumerate(line):
            if char == ".":
                continue
            else:
                antennae[char].append([idx, idy])
    return antennae


def parse_input(input: str) -> Antennamap:
    amap = Antennamap()
    amap.map = [list(line) for line in input.split("\n")]
    amap.ymax = len(amap.map)
    # assume all lines are equal lenght, so we can use the first line
    amap.xmax = len(amap.map[0])
    amap.antennae = locate_antennae(citymap=amap.map)

    return amap


def withinbounds(point: np.array, amap: Antennamap) -> bool:
    return (
        point[0] >= 0
        and point[1] >= 0
        and point[0] < amap.xmax
        and point[1] < amap.ymax
    )


def calc_antinodes(pair: list[list[int]], amap: Antennamap) -> list[tuple[int]]:
    p0 = np.array(pair[0])
    p1 = np.array(pair[1])
    delta = p1 - p0
    all_antinodes = [tuple(p0), tuple(p1)]
    # instead of just on antinodes calc all within bounds including the original positions
    # positive
    p = p1 + delta
    while withinbounds(point=p, amap=amap):
        all_antinodes += [tuple(p)]
        p += delta
    # negative
    p = p0 - delta
    while withinbounds(point=p, amap=amap):
        all_antinodes += [tuple(p)]
        p -= delta

    return all_antinodes


def prune_antinodes(antinodes: list[np.array], amap: Antennamap) -> list[tuple[int]]:
    # skip out of bounds check as we already did when we added them.

    # remove duplicates
    return list(set(antinodes))


def get_all_antinodes(amap: Antennamap) -> list[tuple[int]]:
    antinodes = []
    for key in amap.antennae:
        # generate all 2 permunations of antennaeu of same type:
        combis = list(itertools.combinations(amap.antennae[key], r=2))
        for pair in combis:
            antinodes += calc_antinodes(pair=pair, amap=amap)

    # prune
    antinodes = prune_antinodes(antinodes=antinodes, amap=amap)
    return antinodes


def run_all(input: str) -> int:
    amap = parse_input(input=input)
    antinodes = get_all_antinodes(amap=amap)
    return len(antinodes)


import time

t0 = time.time()
input_path = "input/dec8.txt"

with open(input_path) as f:
    input = f.read()


val = run_all(input=input)
print(f"antinodes count: {val}")

t1 = time.time()
print(f"time: {(t1-t0)} secunds")
