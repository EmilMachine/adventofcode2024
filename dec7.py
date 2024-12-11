from enum import Enum
from operator import add, mul
from typing import List


class Op(Enum):
    MUL = mul
    ADD = add

    def __call__(self, *args):
        return self.value(*args)


def parse_input(input: str) -> List[List[int]]:
    out = []
    for line in input.split("\n"):
        if len(line) > 0:
            kv = line.split(":")
            out.append([int(kv[0])] + list(map(int, kv[1].strip().split(" "))))
    return out


def reduce_one(line: List[int], op: Op) -> List[int]:
    line[1] = op(line[0], line[1])
    return line[1:]


def reducer(line: List[int], target: int) -> bool:
    if len(line) == 1:
        return line[0] == target
    left = reducer(reduce_one(line.copy(), Op.MUL), target)
    right = reducer(reduce_one(line.copy(), Op.ADD), target)
    return right or left


def is_matchable(line: List[int]) -> bool:
    key = line[0]
    vals = line[1:]
    return reducer(vals, key)


def sum_valid(input: str) -> int:
    out_sum = 0
    input = parse_input(input)
    for line in input:
        if is_matchable(line):
            out_sum += line[0]
    return out_sum


input_path = "input/dec7.txt"

with open(input_path) as f:
    input = f.read()

val = sum_valid(input=input)
print(f"checksum sum {val}")
