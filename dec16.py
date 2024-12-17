# algo idea
# Read map
# Spawn raindeers at any intersection
# (never let raindeer backtrack) (revisit location)
# retrun the raindeer with the lowest score

import copy
from itertools import compress

from pydantic import BaseModel


class Room(BaseModel):
    plan: list[list[str]]
    goal: tuple[int, int]


class Raindeer(BaseModel):
    score: int = 0
    direction: tuple[int, int] = (0, 1)
    position: tuple[int, int]
    visited: list[tuple[int, int]] = []
    visited_dir: list[str] = []
    stuck: bool = False


def get_goal(plan: list[list[int]]) -> tuple[int]:
    for row, row_list in enumerate(plan):
        for col, _ in enumerate(row_list):
            if plan[row][col] == "E":
                return (row, col)


# Iterate over the linked list and apply splits
def parse_input(input: str) -> Room:
    room_plan = []
    for line in input.split("\n"):
        # update roomplan to new rules
        room_plan.append(list(line))

    goal = get_goal(plan=room_plan)
    room = Room(plan=room_plan, goal=goal)
    return room


def get_raindeer(room: Room) -> Raindeer:
    for row, row_list in enumerate(room.plan):
        for col, _ in enumerate(row_list):
            if room.plan[row][col] == "S":
                return Raindeer(
                    position=(row, col), visited=[(row, col)], visited_dir=[">"]
                )


def move_raindeer(raindeer: Raindeer, dir: tuple[int, int]) -> Raindeer:
    pos = raindeer.position
    new_pos = (pos[0] + dir[0], pos[1] + dir[1])
    raindeer.position = new_pos
    raindeer.score += 1000 * (dir != raindeer.direction) + 1
    raindeer.direction = dir
    raindeer.visited.append(new_pos)
    dir_dict = {(1, 0): "v", (-1, 0): "^", (0, 1): ">", (0, -1): "<"}
    raindeer.visited_dir.append(dir_dict[dir])
    return raindeer


def plot_explored(room: Room, deers: list[Raindeer]) -> None:
    tmp_plan = copy.deepcopy(room.plan)

    for deer in deers:
        for count, step in enumerate(deer.visited):
            tmp_plan[step[0]][step[1]] = deer.visited_dir[count]  # str(count % 10)
    for line in tmp_plan:
        print("".join(line))


def race_raindeer(
    room: Room, raindeer: Raindeer, verbose: bool = False, update: int = 0
) -> list[Raindeer]:
    racing_raindeers = [raindeer]
    stuck_raindeers = []
    finished_raindeers = []
    step = 0

    while len(racing_raindeers) > 0:
        step += 1
        if update > 0 and step % update == 0:
            print(f"~ ~ step: {step} ~ ~")
            print(f"racing deers: {len(racing_raindeers)}")
            print(f"racing deers: {len(stuck_raindeers)}")
            print(f"racing deers: {len(finished_raindeers)}")

            # plot_explored(room=room, deers=racing_raindeers + stuck_raindeers)

        # if verbose:
        #     print(
        #         step,
        #         len(racing_raindeers),
        #         [r.position for r in racing_raindeers],
        #         room.goal,
        #     )
        new_deers = []
        # update next move
        for raindeer in racing_raindeers:
            dir = raindeer.direction
            pos = raindeer.position
            directions = (dir, (dir[1], -1 * dir[0]), (-1 * dir[1], dir[0]))
            new_pos = [(pos[0] + r, pos[1] + c) for r, c in directions]
            is_legal = [
                room.plan[r][c] != "#" and (r, c) not in raindeer.visited
                for r, c in new_pos
            ]

            dir_options = list(compress(directions, is_legal))

            if len(dir_options) == 0:
                raindeer.stuck = True
            elif len(dir_options) == 1:
                move_raindeer(raindeer=raindeer, dir=dir_options[0])
            elif len(dir_options) > 1:
                first_dir = dir_options.pop()

                # spawn new raindeers
                new_deers += [
                    move_raindeer(raindeer=copy.deepcopy(raindeer), dir=dir)
                    for dir in dir_options
                ]

                # move after
                move_raindeer(raindeer=raindeer, dir=first_dir)

        # append new raindeers
        racing_raindeers += new_deers

        # check for goal
        for raindeer in racing_raindeers:
            if raindeer.position == room.goal:
                raindeer.stuck = True
                finished_raindeers.append(raindeer)

        # remove stuck raindeers (maybe better way)
        if verbose:
            # print stuck raindeer
            for raindeer in racing_raindeers:
                if raindeer.stuck:
                    pos = raindeer.position
                    print(
                        raindeer.position,
                        raindeer.direction,
                    )
                    d = 3
                    lines = room.plan[pos[0] - d : pos[0] + d + 1]
                    for l in lines:
                        print("".join(l[pos[1] - d : pos[1] + d + 1]))
        stuck_raindeers += [raindeer for raindeer in racing_raindeers if raindeer.stuck]

        racing_raindeers = [
            raindeer for raindeer in racing_raindeers if not raindeer.stuck
        ]

    return finished_raindeers


def flood_fill(room: Raindeer, raindeer: Raindeer):
    inside = []
    checked = []
    tocheck = [raindeer.position]

    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
    while len(tocheck) > 0:
        r, c = tocheck.pop()
        if room.plan[r][c] == "#":
            checked.append((r, c))
        else:
            inside.append((r, c))
            potential_check = [(r + dr, c + dc) for dr, dc in dirs]
            real_to_check = [
                (r, c)
                for r, c in potential_check
                if not ((r, c) in inside or (r, c) in checked)
            ]
            tocheck += real_to_check
    print("goal is in fill", room.goal in inside)
    return inside


def run_all(input: str) -> int:
    room = parse_input(input=input)
    raindeer = get_raindeer(room=room)

    # flood_fill(room=room, raindeer=raindeer)
    min_score = -1

    win_deers = race_raindeer(room=room, raindeer=raindeer, verbose=False, update=100)
    min_score = min([deer.score for deer in win_deers])

    # # get windeer.
    # for deer in win_deers:
    #     if deer.score == min_score:
    #         win_deer = deer
    # # plot it.
    # tmp_plan = room.plan
    # for count, step in enumerate(win_deer.visited):
    #     tmp_plan[step[0]][step[1]] = win_deer.visited_dir[count]  # str(count % 10)
    # for line in tmp_plan:
    #     print("".join(line))

    return min_score


import time

t0 = time.time()
input_path = "input/dec16.txt"

with open(input_path) as f:
    input = f.read()


val = run_all(input=input)

print(f"safety number: {val}")

t1 = time.time()
print(f"time: {(t1-t0)} seconds")
