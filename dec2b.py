from typing import List

import numpy as np

input_path = "input/dec2.txt"

with open(input_path) as f:
    input = f.read()


def safe_check(*, sign: int, diff: int) -> bool:
    if sign * diff < 1 or sign * diff > 3:
        # Check violation of stafety.
        # not 1-3 diff in the sign direction
        return False
    return True


def assess_safety(seq: List[int]) -> bool:
    if assess_safety_notfirst(seq):
        return True
    else:
        # Check with first removed
        if assess_safety_notfirst(seq=seq[1:], remove_count=1):
            return True
    return False


def assess_safety_notfirst(seq: List[int], remove_count: int = 0) -> bool:
    # we can do one removal
    # check removal of all but first digit
    idx = 0
    sign = 0
    while idx < len(seq) - 1:
        curr = seq[idx]
        next = seq[idx + 1]
        diff = next - curr
        if sign == 0 and diff != 0:
            # assign the initial direction
            sign = np.sign(diff)

        if not safe_check(sign=sign, diff=diff):
            remove_count += 1
            if remove_count > 1:
                # if we already removed discard
                return False
            else:
                # if only last digit violates, return true
                if idx == len(seq) - 2:
                    return True

                # Skip
                # compute skip, discard if also not safe
                diff = seq[idx + 2] - seq[idx]
                if not safe_check(sign=sign, diff=diff):
                    return False
                # skip ahead
                idx += 1

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
