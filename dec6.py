from enum import Enum
from typing import List

from pydantic import BaseModel

# algo
# read input room + guard
# check ahead of guard
# move guard
# leave trail
# count trail


class Guard(BaseModel):
    x: int = 0
    y: int = 0
    xdir: int = 0
    ydir: int = -1


class PathState(str, Enum):
    FREE = "free"
    BLOCKED = "blocked"
    OUT = "out"


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
    return PathState.FREE


def turn_guard(guard: Guard) -> Guard:
    # turn 90 degrees right
    # (-y,x)
    guard.xdir, guard.ydir = (-1 * guard.ydir, guard.xdir)
    return guard


def walk_guard(room: List[List[str]], guard: Guard) -> List[List[str]]:
    # leave trail:
    room[guard.y][guard.x] = "1"
    # check ahead:
    state = check_ahead(room=room, guard=guard)
    while state != PathState.OUT:
        if state == PathState.BLOCKED:
            guard = turn_guard(guard)
        if state == PathState.FREE:
            # move guard
            guard.x += guard.xdir
            guard.y += guard.ydir
            # leave trail
            room[guard.y][guard.x] = "1"
        state = check_ahead(room=room, guard=guard)

    # we end up in the PathState.OUT (return room)
    return room


def count_room_path(room: List[List[str]]) -> int:
    count = 0
    for line in room:
        count += line.count("1")
    return count


def restore_room(room: List[List[str]]) -> str:
    return "\n".join(["".join(i) for i in room])


def simulate_guard(input: str) -> int:
    room = parse_input(input)
    guard = find_start_position(room=room)
    room = walk_guard(room=room, guard=guard)
    # print(restore_room(room=room))
    return count_room_path(room=room)


input_path = "input/dec6.txt"

with open(input_path) as f:
    input = f.read()

val = simulate_guard(input=input)
print(f"tiles viseted: {val}")
