# algo idea
# read in and parse row col grid.
# Find the first row,col not mapped.
# start with it and grow the patch. (keep track of area + perimeter)
# stop when growing is no longer possible
# return area,perimeter + used coordinates
# Go to next unused coordinate

# figure out how to figure out sides.
# IDEAS
# n-corners = n-sidse .
# but corners are easier to check for?
# other way check for double sided parrallel edge adn sub track from total
# or just find edges and only cound uniu

# actual algo
# check vertical and horizontal seperately
# Find all over edges, and only count those that don't have one next to it.
# Find all lower edges, do the same.

# shorter elegant solution see:
# -https://www.reddit.com/r/adventofcode/comments/1hcdnk0/comment/m1p47qp/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button

import numpy as np
from pydantic import BaseModel


class Field(BaseModel):
    vals: list[list[str]] = []
    row_max: int = 0
    col_max: int = 0


class Subfield(BaseModel):
    val: str = ""
    area: int = 0
    perimeter: int = 0
    places: list[tuple[int]] = []
    checked: list[tuple[int]] = []
    to_check: list[tuple[int]] = []


# Iterate over the linked list and apply splits
def parse_input(input: str) -> Field:
    field = Field
    field.vals = [list(row) for row in input.split("\n")]
    field.row_max = len(field.vals)
    field.col_max = len(field.vals[0])
    return field


def grow_subfield(sub: Subfield, field: Field) -> Subfield:
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    edge_change = {
        0: 4,
        1: 2,
        2: 0,
        3: -2,
        4: -4,
    }
    while len(sub.to_check) > 0:
        f = sub.to_check.pop()
        if field.vals[f[0]][f[1]] == sub.val:
            sub.places.append(f)
            potential_new = [
                (f[0] + i, f[1] + j)
                for i, j in directions
                if (f[0] + i) >= 0
                and (f[0] + i) < field.row_max
                and (f[1] + j) >= 0
                and f[1] + j < field.col_max
            ]

            real_new = [
                p
                for p in potential_new
                if p not in sub.places
                and p not in sub.checked
                and p not in sub.to_check
            ]
            sub.to_check += real_new
            sub.area += 1
            neighbors = sum([p in sub.places for p in potential_new])
            sub.perimeter += edge_change[neighbors]
            # update perimeter
        else:
            sub.checked.append(f)
    return sub


def update_subfield(field: Field, row: int, col: int) -> Subfield:
    sub = Subfield()
    sub.val = field.vals[row][col]
    sub.to_check = [(row, col)]

    sub = grow_subfield(sub=sub, field=field)
    return sub


def count_straightside(sub: Subfield) -> int:
    places = sub.places

    top_edges = [(r, c) for r, c in places if (r - 1, c) not in places]
    unique_top_edges = len(
        [(r, c) for r, c in top_edges if (r, c + 1) not in top_edges]
    )

    buttom_edges = [(r, c) for r, c in places if (r + 1, c) not in places]
    unique_buttom_edges = len(
        [(r, c) for r, c in buttom_edges if (r, c + 1) not in buttom_edges]
    )

    left_edges = [(r, c) for r, c in places if (r, c - 1) not in places]
    unique_left_edges = len(
        [(r, c) for r, c in left_edges if (r + 1, c) not in left_edges]
    )

    right_edges = [(r, c) for r, c in places if (r, c + 1) not in places]
    unique_rihgt_edges = len(
        [(r, c) for r, c in right_edges if (r + 1, c) not in right_edges]
    )
    unique_edges = (
        unique_top_edges + unique_buttom_edges + unique_left_edges + unique_rihgt_edges
    )
    # print(unique_top_edges, unique_buttom_edges, unique_left_edges, unique_rihgt_edges)
    return unique_edges


def run_all(input: str) -> int:
    field = parse_input(input=input)
    counted = []
    subs = []
    check_sum = 0

    for row in range(field.row_max):
        for col in range(field.col_max):
            if (row, col) not in counted:
                sub = update_subfield(field=field, row=row, col=col)
                subs.append(sub)
                counted += sub.places

    for sub in subs:
        check_sum += sub.area * count_straightside(sub=sub)

    return check_sum


import time

t0 = time.time()
input_path = "input/dec12.txt"

with open(input_path) as f:
    input = f.read()


val = run_all(input=input)

print(f"feence checksum: {val}")

t1 = time.time()
print(f"time: {(t1-t0)} secunds")
