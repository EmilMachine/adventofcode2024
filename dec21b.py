# algo idea
# make some dicts that map all from X->Y combination
# For each layer
# Apply translation each level up.
# Calc final checksums
## Instead of applying it keep track of the pairwise combinations
## at the end sum them together with cost

from collections import defaultdict

# row, col
NUM_KEYBOARD = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}

# row, col
DIR_KEYBOARD = {"^": (0, 1), "A": (0, 2), "<": (1, 0), "v": (1, 1), ">": (1, 2)}


# Iterate over the linked list and apply splits
def parse_input(input: str) -> dict[str, int]:
    out = {}
    for s in input.split("\n"):
        out[s] = int(s[:-1])
    return out


def get_paths(v1, v2, forbidden):
    dr = v2[0] - v1[0]
    dc = v2[1] - v1[1]
    if dr > 0:
        rsign = "v"
    else:
        rsign = "^"
    if dc > 0:
        csign = ">"
    else:
        csign = "<"
    dr = abs(dr)
    dc = abs(dc)

    # return row first , colfirst options
    options = (dr * rsign + dc * csign + "A", dc * csign + dr * rsign + "A")
    if options[0] == options[1]:
        options = (options[0],)
    elif (v1[0], v2[1]) == forbidden:
        # colfirst
        options = (options[0],)
    elif (v2[0], v1[1]) == forbidden:
        # rowfirst
        options = (options[1],)

    return options


def get_num_to_dict():
    converter = {}
    forbidden = (3, 0)
    for n1, v1 in NUM_KEYBOARD.items():
        for n2, v2 in NUM_KEYBOARD.items():
            converter[n1 + n2] = get_paths(v1=v1, v2=v2, forbidden=forbidden)
    return converter


def get_dir_to_dict():
    converter = {}
    forbidden = (0, 0)
    for n1, v1 in DIR_KEYBOARD.items():
        for n2, v2 in DIR_KEYBOARD.items():
            converter[n1 + n2] = get_paths(v1=v1, v2=v2, forbidden=forbidden)
    return converter


def get_count_dir(code):
    count_dir = defaultdict(int)
    # code = "A" + code
    for i_r1 in range(len(code) - 1):
        text = code[i_r1 : i_r1 + 2]
        count_dir[text] += 1
    return count_dir


def num_translate(
    code: str, meta_dir: dict[str, dict[str, int]], n: int, num_dir: dict[str, str]
) -> int:
    # convert code to count_dir
    count_dir = get_count_dir(code)

    first = num_dir[code[:2]]
    # apply meta_dir n times
    for _ in range(n):
        count_dir_next = defaultdict(int)
        first = "A" + first[0]
        count_dir_next["A" + first[0]] += 1
        for c, val in count_dir.items():
            for new_c, new_val in meta_dir[c].items():
                count_dir_next[new_c] += val * new_val
        count_dir = count_dir_next
        first = num_dir[first]
    return count_dir


def get_cost(count_dir: dict[str, int], cost_dir: dict[str, int]) -> int:
    cost = 0
    for k, v in count_dir.items():
        cost += cost_dir[k] * v
    return cost


def translate(
    code: str,
    num_convert: dict[str, str],
    meta_dir: dict[str, dict[str, int]],
    cost_dir: dict[str, int],
    dir_convert_simple: dict[str, str],
):
    # code <- robot1
    # robot1 <- robot2 (code2)
    # robot2 <- robot3 (code3)
    # robot3 <- me (code4)
    n_bots = 1
    cost = 0
    code = "A" + code
    for i_r1 in range(len(code) - 1):
        text = code[i_r1 : i_r1 + 2]
        codes2 = num_convert[text]
        count_dirs = [
            num_translate(
                code=c, meta_dir=meta_dir, n=n_bots, num_dir=dir_convert_simple
            )
            for c in codes2
        ]
        costs = [
            get_cost(count_dir=count_dir, cost_dir=cost_dir) for count_dir in count_dirs
        ]
        cost += min(costs)
    return cost


def pprint(x):
    for k, v in x.items():
        print(k, v)


def run_all(input: str) -> int:
    codes = parse_input(input)
    num_convert = get_num_to_dict()
    dir_convert = get_dir_to_dict()
    # pprint(num_convert)
    # pprint(dir_convert)

    # we can simplify the dir convert as we always end and start
    # on A so there is no difference in paths
    dir_convert_simple = {}
    for d, item in dir_convert.items():
        dir_convert_simple[d] = item[0]

    meta_dir = {}
    cost_dir = {}
    for d, item in dir_convert_simple.items():
        cost_dir[d] = len(item)
        item = item
        tmp_dir = {}
        for l in range(len(item) - 1):
            text = item[l : l + 2]
            if text in tmp_dir:
                tmp_dir[text] += 1
            else:
                tmp_dir[text] = 1
        meta_dir[d] = tmp_dir
    # print(meta_dir)
    # print(cost_dir)

    correct = {"029A": 68, "980A": 60, "179A": 68, "456A": 64, "379A": 64}
    out = 0
    for code, val in codes.items():
        cost = translate(
            code,
            num_convert=num_convert,
            meta_dir=meta_dir,
            cost_dir=cost_dir,
            dir_convert_simple=dir_convert_simple,
        )
        print(code, cost, f"({correct[code]})")
        out += cost * val
    # print(num_convert)
    # print(dir_convert)
    # print(codes)

    return out


import time

t0 = time.time()
input_path = "input/dec21_test.txt"

with open(input_path) as f:
    input = f.read()

val = run_all(input=input)
print(f"checksum: {val}")
t1 = time.time()
print(f"time: {(t1-t0)} seconds")

# -----

num_convert = get_num_to_dict()
dir_convert = get_dir_to_dict()
# pprint(num_convert)
# pprint(dir_convert)

# we can simplify the dir convert as we always end and start
# on A so there is no difference in paths
dir_convert_simple = {}
for d, item in dir_convert.items():
    dir_convert_simple[d] = item[0]

meta_dir = {}
cost_dir = {}
for d, item in dir_convert_simple.items():
    cost_dir[d] = len(item)
    item = "A" + item
    tmp_dir = defaultdict(int)
    for l in range(len(item) - 1):
        text = item[l : l + 2]
        tmp_dir[text] += 1
    meta_dir[d] = tmp_dir

code = "Av<<A>>^A<A>AvA<^AA>A<vAAA>^A"
cdir = get_count_dir(code)


cost = get_cost(cdir, cost_dir=cost_dir)
print(cost)

import itertools

codes = []
code = "029A"


def numconvert_codes(code: str, num_convert: dict[str, str]):
    code = "A" + code
    codes = []
    for i_r1 in range(len(code) - 1):
        text = code[i_r1 : i_r1 + 2]
        codes2 = num_convert[text]
        if len(codes) > 0:
            codes = list([i + j for i, j in itertools.product(codes, codes2)])
        else:
            codes = list(codes2)
    return codes


codes = numconvert_codes(code=code, num_convert=num_convert)

print(codes[1])

first = codes[1][:2]
cdir1 = get_count_dir(code=codes[1])


count_dir = cdir1
pprint(count_dir)
# pprint(dir_convert_simple)
# pprint(meta_dir)

n = 1
print("----")
# apply meta_dir n times
for _ in range(n):
    count_dir_next = defaultdict(int)
    first = "A" + first[0]
    count_dir[first] += 1
    # print(first)
    for c, val in count_dir.items():
        print(c, val)
        for new_c, new_val in meta_dir[c].items():
            count_dir_next[new_c] += val * new_val
            # print(c, val, count_dir_next)
    count_dir = count_dir_next
    first = dir_convert_simple[first]

# v<<A|>>^A|<A|>A|vA|<^A|A|>A|<vA|A|A|>^A|
# A  <    A  ^  A  >   ^ ^   A  v v v   A

# print(f"cdir = {cdir}")
# print(f"count_dir = {count_dir}")
v1_sum = 0
v2_sum = 0
for k, v in cdir.items():
    print(k, v, count_dir[k])
    v1_sum += v
    v2_sum += count_dir[k]

print(v1_sum, v2_sum)

print(count_dir == cdir)
print(dir_convert_simple["^A"])
print(meta_dir["^A"])
