import re

input_path = "input/dec3.txt"

with open(input_path) as f:
    input = f.read()


def extract_and_sum_multiplications(input_string: str) -> int:
    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    matches = pattern.findall(input_string)
    total_sum = 0

    for x, y in matches:
        total_sum += int(x) * int(y)

    return total_sum


test_input = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"

result = extract_and_sum_multiplications(input)
print(f"Total sum of multiplications: {result}")
