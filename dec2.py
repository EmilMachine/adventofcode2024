from typing import List

import numpy as np

input_path = "input/dec2.txt"

with open(input_path) as f:
    input = f.read()


def assess_safety(seq: List[int]) -> bool:
    idx = 0
    sign = 0
    while idx < len(seq) - 1:
        curr = seq[idx]
        next = seq[idx + 1]
        diff = next - curr
        if sign == 0 and diff != 0:
            # assign the initial direction
            sign = np.sign(diff)
        if sign * diff < 1 or sign * diff > 3:
            # Check violation of stafety.
            # not 1-2 diff in the sign direction
            return False
        idx += 1

    return True


def process_input(input: str) -> int:
    safety_count = 0
    for line in input.split("\n"):
        if len(line) > 0:
            cleanline = [int(i) for i in line.split(" ")]
            if assess_safety(cleanline):
                safety_count += 1

    return safety_count


result = process_input(input)
print(result)
