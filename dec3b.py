import re
from typing import List

input_path = "input/dec3.txt"

with open(input_path) as f:
    input = f.read()


def extract_and_sum_multiplications(input: str) -> int:
    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    matches = pattern.findall(input)
    total_sum = 0

    for x, y in matches:
        total_sum += int(x) * int(y)

    return total_sum


def preprocess(input: str) -> str:
    # remove all segments from don't() --> do() and return the new clean string
    out = ""
    donts = input.split("don't()")
    # grab any string before don't
    out += donts[0]
    if len(donts) > 1:
        for dont in donts[1:]:
            do = dont.split("do()")
            # grab all dos after a don't
            if len(do) > 1:
                out += "".join(do[1:])
    return out


result = extract_and_sum_multiplications(preprocess(input))
print(f"Total sum of multiplications: {result}")
