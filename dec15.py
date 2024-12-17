# algo idea
# Simulate box buses, but don't update the map,
# update the boxes in a dict

import re

import numpy as np
from pydantic import BaseModel


class Bot(BaseModel):
    row: int
    col: int


# class Barral(BaseModel):
#     row: int
#     col: int


class Room(BaseModel):
    plan: list[list[str]]
    instructions: str


def tuple_str2int(input: tuple[str]) -> tuple[int]:
    return tuple(map(int, input))


# Iterate over the linked list and apply splits
def parse_input(input: str) -> Room:
    room_plan = []
    instructions = ""
    for line in input.split("\n"):
        if "#" in line:
            room_plan.append(list(line))
        elif len(line) > 0:
            instructions += line

    room = Room(plan=room_plan, instructions=instructions)

    return room


def get_bot(room: Room) -> Bot:
    for row, row_list in enumerate(room.plan):
        for col, _ in enumerate(row_list):
            if room.plan[row][col] == "@":
                return Bot(row=row, col=col)


def get_barrels(room: Room) -> dict[tuple[int] : int]:
    Barrals = {}
    for row, row_list in enumerate(room.plan):
        for col, _ in enumerate(row_list):
            if room.plan[row][col] == "O":
                Barrals[(row, col)] = 1

    return Barrals


def is_moveable(
    barrals: dict[tuple[int], int], room: Room, v: tuple[int], pos: tuple[int]
) -> bool:
    if pos in barrals:
        new_pos = (pos[0] + v[0], pos[1] + v[1])
        moveable = is_moveable(barrals=barrals, room=room, v=v, pos=new_pos)

        if moveable:
            # update barral if no wall was hit - as sideeffect
            del barrals[pos]
            barrals[new_pos] = 1
        return moveable

    else:
        if room.plan[pos[0]][pos[1]] == "#":
            return False
        return True


def move_bot(
    instruction: str, bot: Bot, room: Room, barrals: dict[tuple[int], int]
) -> Bot:
    direction_map = {"<": (0, -1), "^": (-1, 0), ">": (0, 1), "v": (1, 0)}
    v = direction_map[instruction]
    new_bot_pos = (bot.row + v[0], bot.col + v[1])
    moveable = is_moveable(barrals=barrals, room=room, v=v, pos=new_bot_pos)
    if moveable:
        bot.row = new_bot_pos[0]
        bot.col = new_bot_pos[1]
    return bot


def print_map(room: Room, bot: Bot, barrals: dict[tuple[int], int]) -> None:
    print_map = []
    # clean map
    for line in room.plan:
        print_map.append(list("".join(line).replace("O", ".").replace("@", ".")))
    # Append robot
    print_map[bot.row][bot.col] = "@"
    # append Barrals
    for barral in barrals:
        print_map[barral[0]][barral[1]] = "O"
    # putting the map together
    print_map = "\n".join(["".join(i) for i in print_map])

    print(print_map)


def run_all(input: str) -> int:
    room = parse_input(input=input)
    bot = get_bot(room=room)
    barrels = get_barrels(room=room)

    verbose = False
    # verbose = True
    if verbose:
        print("room:", room.plan)
        print("instructions:", room.instructions)
        print("bot", bot.row, bot.col)
        for barrel in barrels:
            print(barrel)
    # move
    for i in room.instructions:
        bot = move_bot(instruction=i, bot=bot, room=room, barrals=barrels)
        # print(i)
        # print_map(room=room, bot=bot, barrals=barrels)
    # calc barrals
    bsum = 0
    for b in barrels:
        bsum += b[0] * 100 + b[1]

    print_map(room=room, bot=bot, barrals=barrels)

    return bsum


import time

t0 = time.time()
input_path = "input/dec15.txt"

with open(input_path) as f:
    input = f.read()


val = run_all(input=input)

print(f"safety number: {val}")

t1 = time.time()
print(f"time: {(t1-t0)} seconds")
