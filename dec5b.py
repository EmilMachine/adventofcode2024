# Algo outline

# Parse rules and inputs.
# Algo for verifying correct / non-viloating order
# A) figure out rules that applies
# B) compare indices
# Fix wrong codes
# A) Go through rules
# B) For each rule that is violated switch the numbers.
# C) go through again until it is fixed.
# grab middle numbers and add
from typing import List

from pydantic import BaseModel


class Safety(BaseModel):
    rules: List[List[int]]
    manuals: List[List[int]]


def parse_input(input: str) -> Safety:
    rules = []
    manuals = []
    for line in input.split("\n"):
        # rule
        if "|" in line:
            rules.append(line.split("|"))
        # manual
        if "," in line:
            manuals.append(line.split(","))
    return Safety(rules=rules, manuals=manuals)


def validate_input(rules: List[List[int]], manual: list[int]) -> bool:
    manual_set = set(manual)
    for rule in rules:
        # A) The rule shold apply and B) it is incorrect
        if len(set(rule) & manual_set) == 2 and manual.index(rule[0]) > manual.index(
            rule[1]
        ):
            return False
    return True


def fix_wrong_manual(rules: List[List[int]], manual: List[int]) -> List[int]:
    manual_set = set(manual)
    for rule in rules:
        # A) The rule shold apply and B) it is incorrect
        if len(set(rule) & manual_set) == 2 and manual.index(rule[0]) > manual.index(
            rule[1]
        ):
            idx0 = manual.index(rule[0])
            idx1 = manual.index(rule[1])
            # switch
            manual[idx0] = rule[1]
            manual[idx1] = rule[0]
    if not validate_input(rules=rules, manual=manual):
        manual = fix_wrong_manual(rules=rules, manual=manual)

    return manual


def sum_middle_fixed(safety: Safety) -> int:
    middle = 0
    for manual in safety.manuals:
        # correct manual
        if not validate_input(safety.rules, manual):
            # fix and add middle
            manual = fix_wrong_manual(rules=safety.rules, manual=manual)
            middle += manual[len(manual) // 2]
    return middle


input_path = "input/dec5.txt"

with open(input_path) as f:
    input = f.read()

val = sum_middle_fixed(safety=parse_input(input))
print(f"middle fixed manual sum: {val}")
