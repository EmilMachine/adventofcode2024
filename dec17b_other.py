# FROM https://github.com/gid/AoC/blob/main/src/aoc/2024/day17.py

example_input = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

REG_A, REG_B, REG_C = "A", "B", "C"
ADV, BXL, BST, JNZ, BXC, OUT, BDV, CDV = 0, 1, 2, 3, 4, 5, 6, 7


def combo_operand(operand: int, regs: dict[str, int]) -> int:
    return operand if operand <= 3 else regs[{4: REG_A, 5: REG_B, 6: REG_C}[operand]]


def run_program(program: list[int], initial_a: int) -> list[int]:
    """Run the program and return the output using the following opcodes:
    adv/bdv/cdv - operations that take right hand bits from A and put them into A/B/C
    bxl/bxc     - operations that flip bits in B
    bst/out     - operations that puts the last 3 bits of something into B or output
    jnz         - operation that controls the program flow (jumps if A!=0)
    """
    regs = {REG_A: initial_a, REG_B: 0, REG_C: 0}
    pointer, output = 0, []
    while pointer < len(program):
        opcode, operand = program[pointer], program[pointer + 1]
        pointer += 2
        if opcode == ADV:
            regs[REG_A] = regs[REG_A] // (2 ** combo_operand(operand, regs))
        elif opcode == BDV:
            regs[REG_B] = regs[REG_A] // (2 ** combo_operand(operand, regs))
        elif opcode == CDV:
            regs[REG_C] = regs[REG_A] // (2 ** combo_operand(operand, regs))
        elif opcode == BXL:
            regs[REG_B] = regs[REG_B] ^ operand
        elif opcode == BXC:
            regs[REG_B] = regs[REG_B] ^ regs[REG_C]
        elif opcode == BST:
            regs[REG_B] = combo_operand(operand, regs) % 8
        elif opcode == OUT:
            output.append(combo_operand(operand, regs) % 8)
        elif opcode == JNZ:
            pointer = pointer if regs[REG_A] == 0 else operand
    return output


def reverse_engineer(loop: list[int], target: list[int], a_so_far: int = 0) -> int:
    """Find the value of register A that will output the specified target"""
    if target == []:
        return a_so_far
    for candidate_a in (a_so_far * 8 + next_3_bits for next_3_bits in range(8)):
        # Extend register A by 3 bits and see if we output the last token in the target
        if run_program(loop, candidate_a).pop() == target[-1]:
            try:
                return reverse_engineer(loop, target[:-1], candidate_a)
            except StopIteration:
                continue
    raise StopIteration


def solve(inputs: str):
    registers_input, program_input = inputs.split("\n\n")
    program = list(map(int, program_input[8:].split(",")))
    initial_a = int(registers_input.splitlines()[0][12:])

    print(f"Part 1: {','.join(map(str, run_program(program, initial_a)))}")

    assert program[-2:] == [JNZ, 0]  # i.e. this is a program that loops until A is 0
    loop = program[:-2]
    initial_a = reverse_engineer(loop, program)
    assert run_program(program, initial_a) == program
    print(f"Part 2: {initial_a}\n")


input_path = "input/dec17.txt"
with open(input_path) as f:
    input = f.read()

# solve(example_input)
actual_input = input

solve(actual_input)
