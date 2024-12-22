# algo idea
# make some dicts that map all from X->Y combination
# For each layer
# Apply translation each level up.
# Calc final checksums
import itertools

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


def num_translate(codes: list[str], dir_convert) -> list[str]:
    total_out = []
    for c in codes:
        out = []
        c = "A" + c
        for i_r1 in range(len(c) - 1):
            text = c[i_r1 : i_r1 + 2]
            codes2 = dir_convert[text]
            if len(out) > 0:
                out = list([i + j for i, j in itertools.product(out, codes2)])
            else:
                out = list(codes2)
        total_out += out
    return total_out


def translate(code: str, num_convert: dict[str, str], dir_convert: dict[str, str]):
    # code <- robot1
    # robot1 <- robot2 (code2)
    # robot2 <- robot3 (code3)
    # robot3 <- me (code4)
    out = ""
    code = "A" + code
    for i_r1 in range(len(code) - 1):
        text = code[i_r1 : i_r1 + 2]
        codes2 = num_convert[text]
        codes3 = num_translate(codes=codes2, dir_convert=dir_convert)
        codes4 = num_translate(codes=codes3, dir_convert=dir_convert)
        if code == "A456A":
            for c in codes4:
                print(text, c)

        tmp = min(codes4, key=len)
        out += tmp
    return out

    # for c2 in code2:
    #     for i_r2 in range(len(c2) - 1):
    #         text = c2[i_r2 : i_r2 + 2]
    #         code3 += dir_convert[text]


def run_all(input: str) -> int:
    codes = parse_input(input)
    num_convert = get_num_to_dict()
    dir_convert = get_dir_to_dict()

    out = 0
    for code, val in codes.items():
        press = translate(code, num_convert=num_convert, dir_convert=dir_convert)
        print(code, len(press))
        out += len(press) * val
    # print(num_convert)
    # print(dir_convert)
    # print(codes)

    return out


import time

t0 = time.time()
input_path = "input/dec21.txt"

with open(input_path) as f:
    input = f.read()

val = run_all(input=input)
print(f"checksum: {val}")
t1 = time.time()
print(f"time: {(t1-t0)} seconds")
print(f"time: {(t1-t0)} seconds")
