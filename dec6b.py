import copy
from enum import Enum
from typing import List

from pydantic import BaseModel

# == ALGO ==
# read input room + guard
# check ahead of guard
# move guard
# leave trail
# count trail

## Loop trough trail from last position for possible obstacles.
# Add obstacle
# Simulate guard and see if we get a loop (or out)
# We will need to hit a position and direction to be a loop
# Update trail lay down direction 0, 90, 180, 270


class Guard(BaseModel):
    x: int = 0
    y: int = 0
    xdir: int = 0
    ydir: int = -1
    dir: int = 0


class PathState(str, Enum):
    FREE = "free"
    BLOCKED = "blocked"
    OUT = "out"
    LOOP = "loop"


def parse_input(input: str) -> List[List[str]]:
    return [list(i) for i in input.split("\n")]


def find_start_position(room: List[List[str]]) -> Guard:
    for idy, line in enumerate(room):
        if "^" in line:
            x0 = line.index("^")
            y0 = idy
    return Guard(x=x0, y=y0, xdir=0, ydir=-1)


def is_out_of_bounds(room: List[List[str]], x: int, y: int) -> bool:
    if x < 0 or y < 0:
        return True
    if y >= len(room):
        return True
    if x >= len(room[y]):
        return True
    return False


def check_ahead(room: List[List[str]], guard: Guard) -> PathState:
    x_next = guard.x + guard.xdir
    y_next = guard.y + guard.ydir

    if is_out_of_bounds(room=room, x=x_next, y=y_next):
        return PathState.OUT
    if room[y_next][x_next] == "#":
        return PathState.BLOCKED
    if str(guard.dir) in room[y_next][x_next]:
        return PathState.LOOP
    return PathState.FREE


def turn_guard(guard: Guard) -> Guard:
    # turn 90 degrees right
    # (-y,x)
    guard.xdir, guard.ydir = (-1 * guard.ydir, guard.xdir)
    guard.dir = (guard.dir + 1) % 4
    return guard


def walk_guard(room: List[List[str]], guard: Guard) -> List[List[str]]:
    # leave trail:
    room[guard.y][guard.x] = "1"
    # check ahead:
    state = check_ahead(room=room, guard=guard)
    while state != PathState.OUT:
        if state == PathState.BLOCKED:
            guard = turn_guard(guard)
        if state == PathState.FREE or state == PathState.LOOP:
            # move guard
            guard.x += guard.xdir
            guard.y += guard.ydir
            # leave trail
            room[guard.y][guard.x] = "1"
        state = check_ahead(room=room, guard=guard)

    # we end up in the PathState.OUT (return room)
    return room


def is_guard_loop(room: List[List[str]], guard: Guard) -> bool:
    # Addend direction
    room[guard.y][guard.x] += str(guard.dir)
    # check ahead:
    state = check_ahead(room=room, guard=guard)
    while state not in (PathState.OUT, PathState.LOOP):
        if state == PathState.BLOCKED:
            guard = turn_guard(guard)
        if state == PathState.FREE:
            # move guard
            guard.x += guard.xdir
            guard.y += guard.ydir
            # leave trail
            room[guard.y][guard.x] += str(guard.dir)
        state = check_ahead(room=room, guard=guard)

    if state == PathState.OUT:
        return False
    if state == PathState.LOOP:
        return True


def count_room_path(room: List[List[str]]) -> int:
    count = 0
    for line in room:
        count += line.count("1")
    return count


def restore_room(room: List[List[str]]) -> str:
    return "\n".join(["".join(i) for i in room])


def get_obstacle_path(room: List[List[str]]) -> List[List[int]]:
    possible_obstacles = []
    for idy, line in enumerate(room):
        possible_obstacles += [(idx, idy) for idx, x in enumerate(line) if x == "1"]
    return possible_obstacles


def simulate_guard(input: str) -> int:
    initial_room = parse_input(input)
    initial_guard = find_start_position(room=initial_room)
    room = walk_guard(
        room=copy.deepcopy(initial_room), guard=initial_guard.model_copy()
    )
    possible_obstacles = get_obstacle_path(room=room)
    loop_count = 0
    try_count = 0
    for x, y in possible_obstacles:
        try_count += 1
        print(x, y, try_count, len(possible_obstacles))
        # skip inital guard position
        if x == initial_guard.x and y == initial_guard.y:
            continue
        # reset room and guard
        room = copy.deepcopy(initial_room)
        guard = initial_guard.model_copy()
        # place obstacle
        room[y][x] = "#"
        # check loop
        if is_guard_loop(room=room, guard=guard):
            loop_count += 1
            # print(x, y)
    return loop_count

    # print(restore_room(room=room))


input_path = "input/dec6.txt"

import time

with open(input_path) as f:
    input = f.read()
t0 = time.time()

val = simulate_guard(input=input)
print(f"Possible loops: {val}")
t1 = time.time()
print(f"time: {t1-t0}")

# Possible loops: 1976
# time: 98.68892407417297
