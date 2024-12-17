# algo idea
# Read in all robots
# predict future postition with multiply and modulus
# Count quarants + calc safety sum

import re

import numpy as np
from pydantic import BaseModel


class Bot(BaseModel):
    p: tuple[int] = ()
    v: tuple[int] = ()


class Room(BaseModel):
    wide: int
    tall: int


def tuple_str2int(input: tuple[str]) -> tuple[int]:
    return tuple(map(int, input))


# Iterate over the linked list and apply splits
def parse_input(input: str) -> list[Bot]:
    ps = re.findall(r"p=(\d+),(\d+)", input)
    vs = re.findall(r"v=(-?\d+),(-?\d+)", input)
    bots = []

    for p, v in zip(ps, vs):
        b = Bot()
        b.p = tuple_str2int(p)
        b.v = tuple_str2int(v)

        bots.append(b)
    return bots


def move_bots(bots: list[Bot], room: Room, n_steps: int) -> list[Bot]:
    for bot in bots:
        bot.p = (
            (bot.p[0] + n_steps * bot.v[0]) % room.wide,
            (bot.p[1] + n_steps * bot.v[1]) % room.tall,
        )
    return bots


def count_quadrants(bots: list[Bot], room: Room) -> list[int]:
    quadrant = [0, 0, 0, 0]
    for bot in bots:
        a, b = -1, -1
        if bot.p[0] < room.wide // 2:
            a = 0
        elif bot.p[0] > room.wide // 2:
            a = 1
        if bot.p[1] < room.tall // 2:
            b = 0
        elif bot.p[1] > room.tall // 2:
            b = 1
        qi = a + 2 * b
        if a >= 0 and b >= 0:
            quadrant[qi] += 1
    return quadrant


def print_bots(bots: list[Bot], room: Room):
    for y in range(room.tall):
        x_str = ""
        for x in range(room.wide):
            n = sum([1 for bot in bots if bot.p == (x, y)])
            n_str = str(n)
            if n_str == "0":
                n_str = "."
            if x == room.wide // 2 or y == room.tall // 2:
                n_str = " "
            x_str += n_str
        print(x_str)


def run_all(input: str, is_test: bool = False) -> int:
    bots = parse_input(input=input)

    n_steps = 100
    wide = 101
    tall = 103

    if is_test:
        wide = 11
        tall = 7

    room = Room(wide=wide, tall=tall)
    # for m in machines:
    #     print(m.a, m.b, m.prize)
    # print_bots(bots=bots, room=room)
    bots = move_bots(bots=bots, room=room, n_steps=n_steps)

    # print("/")
    # print_bots(bots=bots, room=room)

    quad = count_quadrants(bots=bots, room=room)
    # print(quad)
    check_sum = quad[0] * quad[1] * quad[2] * quad[3]
    return check_sum


import time

t0 = time.time()
input_path = "input/dec14.txt"

with open(input_path) as f:
    input = f.read()


val = run_all(input=input, is_test=False)

print(f"safety number: {val}")

t1 = time.time()
print(f"time: {(t1-t0)} seconds")
