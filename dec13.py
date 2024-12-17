# algo idea
# parse input
# For each algo determine if it is solveable (with whole numbers)
# if solveable find the best solution.

import re

import numpy as np
from pydantic import BaseModel


class Clawmachine(BaseModel):
    a: tuple[int] = ()
    b: tuple[int] = ()
    prize: tuple[int] = ()


def tuple_str2int(input: tuple[str]) -> tuple[int]:
    return tuple(map(int, input))


# Iterate over the linked list and apply splits
def parse_input(input: str) -> list[Clawmachine]:
    bas = re.findall(r"A:\sX\+(\d+),\sY\+(\d+)", input)
    bbs = re.findall(r"B:\sX\+(\d+),\sY\+(\d+)", input)
    prizes = re.findall(r"Prize:\sX=(\d+),\sY=(\d+)", input)
    machines = []

    for a, b, prize in zip(bas, bbs, prizes):
        m = Clawmachine()
        m.a = tuple_str2int(a)
        m.b = tuple_str2int(b)
        m.prize = tuple_str2int(prize)
        machines.append(m)
    return machines


def solve_machine(machine: Clawmachine, a_weight=3, b_weight=1) -> int:

    v3 = np.array(machine.prize)

    # Coefficients matrix
    A = np.array([machine.a, machine.b]).T

    a, b = np.linalg.solve(A, v3)
    p1 = round(a) * machine.a[0] + round(b) * machine.b[0]
    p2 = round(a) * machine.a[1] + round(b) * machine.b[1]
    is_integer_solution = (p1 == machine.prize[0]) and (p2 == machine.prize[1])

    solution = a_weight * round(a) + b_weight * round(b)

    # print(
    #     machine.a, machine.b, machine.prize, a, b, p1, p2, is_integer_solution, solution
    # )
    if is_integer_solution and a >= 0 and b >= 0:  # and a <= 100 and b <= 100:
        return solution
    return 0


def run_all(input: str) -> int:
    machines = parse_input(input=input)
    # for m in machines:
    #     print(m.a, m.b, m.prize)

    check_sum = 0
    for m in machines:
        check_sum += solve_machine(machine=m, a_weight=3, b_weight=1)

        # check_sum += solve_machine(machine=m, a_weight=1, b_weight=3)

    return check_sum


import time

t0 = time.time()
input_path = "input/dec13.txt"

with open(input_path) as f:
    input = f.read()


val = run_all(input=input)

print(f"clawmachine checksum: {val}")

t1 = time.time()
print(f"time: {(t1-t0)} seconds")
