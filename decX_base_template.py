# algo idea


# Iterate over the linked list and apply splits
def parse_input(input: str) -> list[str]:
    return input.split("\n")


def run_all(input: str) -> int:
    out = -1
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
