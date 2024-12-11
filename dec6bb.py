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
    trail: list[list[int]] = []
    phantom_obstacle: list[int] = []
    id: int = 0


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
    if [guard.x, guard.y, guard.dir] in guard.trail:
        return PathState.LOOP
    if room[y_next][x_next] == "#" or [x_next, y_next] in guard.phantom_obstacle:
        return PathState.BLOCKED
    return PathState.FREE


def turn_guard(guard: Guard) -> Guard:
    # turn 90 degrees right
    # (-y,x)
    guard.trail.append([guard.x, guard.y, guard.dir])
    guard.xdir, guard.ydir = (-1 * guard.ydir, guard.xdir)
    guard.dir = (guard.dir + 1) % 4

    return guard


def walk_guard(
    room: List[List[str]],
    guard: Guard,
    phantom_placed: bool = False,
    count: int = 0,
    guard_path: List[List[int]] = [],
) -> int:
    # guard_path is only used by main guard
    id = 0
    if not phantom_placed:
        guard_path.append([guard.x, guard.y])
    # check ahead:
    state = check_ahead(room=room, guard=guard)
    while state != PathState.OUT and state != PathState.LOOP:
        if state == PathState.BLOCKED:
            guard = turn_guard(guard)

        x_next = guard.x + guard.xdir
        y_next = guard.y + guard.ydir
        # guard_path is only used by main guard
        if not phantom_placed:
            visted_before = [x_next, y_next] in guard_path
            if not visted_before:
                guard_path.append([x_next, y_next])

        if state == PathState.FREE:

            if not phantom_placed and not visted_before:
                # spawn phantom obstacle, and phantom guard
                phantom_guard = guard.model_copy()
                id += 1
                phantom_guard.id = id
                phantom_guard.trail = copy.deepcopy(guard.trail)
                phantom_guard.phantom_obstacle = [[x_next, y_next]]
                count = walk_guard(
                    room=room,
                    guard=phantom_guard,
                    phantom_placed=True,
                    count=count,
                    guard_path=[],  # only used by main guard
                )
            # move guard
            guard.x = x_next
            guard.y = y_next

        state = check_ahead(room=room, guard=guard)

    if state == PathState.LOOP:
        print("obstacle found", guard.phantom_obstacle)
        count += 1
    # we end up in the PathState.OUT (return current count)
    return count


def restore_room(room: List[List[str]]) -> str:
    return "\n".join(["".join(i) for i in room])


def simulate_guard(input: str) -> int:
    room = parse_input(input)
    guard = find_start_position(room=room)
    loop_count = walk_guard(room=room, guard=guard)
    return loop_count


input_path = "input/dec6.txt"


import time

with open(input_path) as f:
    input = f.read()
t0 = time.time()

val = simulate_guard(input=input)
print(f"Possible loops: {val}")
t1 = time.time()
print(f"time: {t1-t0}")

# Possible loops: 1932
# right answer is 1976??? (but it is quicker)
# time: 20.3944308757782
