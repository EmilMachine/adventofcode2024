import re
from typing import List, Tuple

# algo A)
# prep read data so it can be accessed by coordinates
# Find all A
# For each A check if there is a MAS cross (NOT PLUS)


def prep_input(input: str) -> List[str]:
    # Prep inout so we can refer to charcaters by coordinates
    return input.split("\n")


def find_all_a(lines: List[str]) -> List[Tuple[int]]:
    # find all X locations.
    x_positions = []
    for xcord, line in enumerate(lines):
        x_positions += [(xcord, y.span()[0]) for y in re.finditer(r"A", line)]

    return x_positions


def test_position(*, lines: List[str], x0: int, y0: int) -> bool:
    ref_set = {"M", "S"}

    # CROSS
    w1x1 = x0 - 1
    w1y1 = y0 - 1
    w1x2 = x0 + 1
    w1y2 = y0 + 1

    w2x1 = x0 - 1
    w2y1 = y0 + 1
    w2x2 = x0 + 1
    w2y2 = y0 - 1

    try:
        w1 = set([lines[w1x1][w1y1], lines[w1x2][w1y2]])
        w2 = set([lines[w2x1][w2y1], lines[w2x2][w2y2]])
    except IndexError:
        # out of bounds
        return False
    if sum([i < 0 for i in [w1x1, w1y1, w1x2, w1y2, w2x1, w2y1, w2x2, w2y2]]) > 0:
        # negative index (no wrap around)
        return False
    if w1 == ref_set and w2 == ref_set:
        return True

    # no match found return False
    return False


def search_xmax(lines: List[str]) -> int:
    count = 0
    a_positions = find_all_a(lines=lines)
    for x0, y0 in a_positions:
        if test_position(lines=lines, x0=x0, y0=y0):
            count += 1
    return count


input_path = "input/dec4.txt"

with open(input_path) as f:
    input = f.read()

count = search_xmax(lines=prep_input(input))
print(f"Toal MAS cross count: {count}")
