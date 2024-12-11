import re
from typing import List, Tuple

# algo A)
# prep read data so it can be accessed by coordinates
# Find all X
# For each X check the 8 possible direction for a match


input_path = "input/dec4.txt"

with open(input_path) as f:
    input = f.read()


def prep_input(input: str) -> List[str]:
    # Prep inout so we can refer to charcaters by coordinates
    return input.split("\n")


def find_all_x(lines: List[str]) -> List[Tuple[int]]:
    # find all X locations.
    x_positions = []
    for xcord, line in enumerate(lines):
        x_positions += [(xcord, y.span()[0]) for y in re.finditer(r"X", line)]

    return x_positions


def test_direction(
    *, lines: List[str], match: str, x0: int, y0: int, xdir: int, ydir: int
) -> bool:
    for i in range(len(match)):
        x1 = x0 + i * xdir
        y1 = y0 + i * ydir
        if x1 < 0 or y1 < 0:
            # negative index (no wrap around)
            return False
        try:
            next_char = lines[x1][y1]
            if match[i] != next_char:
                # A char position does not match in directions
                return False
        except IndexError:
            # we go out of bounds
            return False
    # All matched
    return True


def search_xmax(lines: List[str]) -> int:
    count = 0
    match = "XMAS"
    dir_count = {}
    directions = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))
    x_positions = find_all_x(lines=lines)
    for x0, y0 in x_positions:
        for xdir, ydir in directions:
            if test_direction(
                lines=lines, match=match, x0=x0, y0=y0, xdir=xdir, ydir=ydir
            ):
                count += 1
                # dir_str = f"{xdir}{ydir}"
                # if dir_str in dir_count:
                #     dir_count[dir_str] += 1
                # else:
                #     dir_count[dir_str] = 1
                # if dir_str == "-1-1":
                #     print(x0, y0)

    return count, dir_count


count, dircount = search_xmax(lines=prep_input(input))
print(f"Toal XMAS count: {count}", dircount)

# Toal XMAS count: 2605
