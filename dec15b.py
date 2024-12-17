# algo idea
# Simulate box buses, but don't update the map,
# update the boxes dict, so it holds both coordinates and update those
# still just use the key af the left corner, but update collition check.


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


def double_room(line: str) -> str:
    return (
        line.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
    )


# Iterate over the linked list and apply splits
def parse_input(input: str) -> Room:
    room_plan = []
    instructions = ""
    for line in input.split("\n"):
        if "#" in line:
            # update roomplan to new rules
            line = double_room(line)
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
            if room.plan[row][col] == "[":
                Barrals[(row, col)] = 1

    return Barrals


def is_moveable(
    barrals: dict[tuple[int], int], room: Room, v: tuple[int], pos: tuple[int]
) -> bool:
    # print("pos_to_check", pos)
    left_in = pos in barrals
    right_in = (pos[0], pos[1] - 1) in barrals
    if left_in or right_in:
        if right_in:
            # set pos to left side
            pos = (pos[0], pos[1] - 1)
        new_pos = (pos[0] + v[0], pos[1] + v[1])

        # positions to check
        if v[0] == 0:
            # left right (just check an extra space away)
            if v[1] == 1:
                pos_to_check = (pos[0], pos[1] + 2)
            else:
                pos_to_check = (pos[0], pos[1] - 1)

            moveable = is_moveable(barrals=barrals, room=room, v=v, pos=pos_to_check)
        else:
            # we know we move up and down
            pos_to_check = (pos[0] + v[0], pos[1])
            pos_to_check_extra = (pos[0] + v[0], pos[1] + 1)

            mov1 = is_moveable(barrals=barrals, room=room, v=v, pos=pos_to_check)
            mov2 = is_moveable(barrals=barrals, room=room, v=v, pos=pos_to_check_extra)
            moveable = mov1 and mov2

        return moveable

    else:
        if room.plan[pos[0]][pos[1]] == "#":
            return False
        return True


def move_barrals(
    barrals: dict[tuple[int], int], v: tuple[int], pos: tuple[int]
) -> None:
    # update barral if no wall was hit - as sideeffect
    left_in = pos in barrals
    right_in = (pos[0], pos[1] - 1) in barrals
    if left_in or right_in:
        if right_in:
            # set pos to left side
            pos = (pos[0], pos[1] - 1)
        new_pos = (pos[0] + v[0], pos[1] + v[1])

        # positions to check
        if v[0] == 0:
            # left right (just check an extra space away)
            if v[1] == 1:
                pos_to_check = (pos[0], pos[1] + 2)
            else:
                pos_to_check = (pos[0], pos[1] - 1)

            move_barrals(barrals=barrals, v=v, pos=pos_to_check)
        else:
            # we know we move up and down
            pos_to_check = (pos[0] + v[0], pos[1])
            pos_to_check_extra = (pos[0] + v[0], pos[1] + 1)

            move_barrals(barrals=barrals, v=v, pos=pos_to_check)
            move_barrals(barrals=barrals, v=v, pos=pos_to_check_extra)
        del barrals[pos]
        barrals[new_pos] = 1


def move_bot(
    instruction: str, bot: Bot, room: Room, barrals: dict[tuple[int], int]
) -> Bot:
    direction_map = {"<": (0, -1), "^": (-1, 0), ">": (0, 1), "v": (1, 0)}
    v = direction_map[instruction]
    new_bot_pos = (bot.row + v[0], bot.col + v[1])
    moveable = is_moveable(barrals=barrals, room=room, v=v, pos=new_bot_pos)
    if moveable:
        move_barrals(barrals, v=v, pos=new_bot_pos)
        bot.row = new_bot_pos[0]
        bot.col = new_bot_pos[1]
    return bot


def print_map(room: Room, bot: Bot, barrals: dict[tuple[int], int]) -> None:
    print_map = []
    # clean map
    for line in room.plan:
        print_map.append(list("".join(line).replace("[]", "..").replace("@", ".")))
    # Append robot
    print_map[bot.row][bot.col] = "@"
    # append Barrals
    for barral in barrals:
        print_map[barral[0]][barral[1]] = "["
        print_map[barral[0]][barral[1] + 1] = "]"
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
    verbose_step = False
    # verbose_step = True
    for i in room.instructions:

        bot = move_bot(instruction=i, bot=bot, room=room, barrals=barrels)
        if verbose_step:
            print(i)
            print_map(room=room, bot=bot, barrals=barrels)

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

# not right answer. too low
# 1501479
