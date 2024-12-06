# Algo outline

# Parse rules and inputs.
# Algo for verifying correct / non-viloating order
# A) figure out rules that applies
# B) check indices of rules.
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


def sum_middle_correct(safety: Safety) -> int:
    middle = 0
    for manual in safety.manuals:
        if validate_input(safety.rules, manual):
            middle += manual[len(manual) // 2]
    return middle


input_path = "input/dec5.txt"

with open(input_path) as f:
    input = f.read()

val = sum_middle_correct(safety=parse_input(input))
print(f"middle manual sum: {val}")
