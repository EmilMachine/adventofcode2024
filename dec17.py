# algo idea
# Try to understand computer
# impplement computer
# Try to run program

import re


class Computer:
    reg_a: int = 0
    reg_b: int = 0
    reg_c: int = 0
    program: list[int] = []
    out: list[int] = []
    pointer: int = 0
    skip_jump: bool = False
    halt: bool = False

    def increment(self):
        if self.skip_jump:
            self.skip_jump = False
        else:
            self.pointer += 2

    def execute_program(self):
        while not self.halt:
            self.execute_step()
        return self.out

    def execute_step(self):
        if self.pointer > len(self.program) - 1:
            self.halt = True
        else:
            operator = self.program[self.pointer]
            x = self.program[self.pointer + 1]
            match operator:
                case 0:
                    self.op0(x)
                case 1:
                    self.op1(x)
                case 2:
                    self.op2(x)
                case 3:
                    self.op3(x)
                case 4:
                    self.op4(x)
                case 5:
                    self.op5(x)
                case 6:
                    self.op6(x)
                case 7:
                    self.op7(x)
            self.increment()

    def print(self):
        print(f"reg_a: {self.reg_a}")
        print(f"reg_b: {self.reg_b}")
        print(f"reg_c: {self.reg_c}")
        print(f"program: {self.program}")
        print(f"out: {self.out}")
        print(
            f"pointer: {self.pointer}, skip_jump: {self.skip_jump}, halt: {self.halt}"
        )

    def get_combo(self, x: int):
        match x:
            case 0:
                return x
            case 1:
                return x
            case 2:
                return x
            case 3:
                return x
            case 4:
                return self.reg_a
            case 5:
                return self.reg_b
            case 6:
                return self.reg_c
        raise ValueError

    def adv_helper(self, x: int):
        tmp = self.reg_a
        for i in range(self.get_combo(x)):
            tmp = tmp / 2
            if tmp < 1:
                break
        return tmp

    def op0(self, x: int):
        # adv
        tmp = self.adv_helper(x)
        self.reg_a = int(tmp)

    def op1(self, x: int):
        # bxl
        self.reg_b = self.reg_b ^ x

    def op2(self, x: int):
        # bst
        self.reg_b = self.get_combo(x) % 8

    def op3(self, x: int):
        # jnz
        if self.reg_a == 0:
            pass
        else:
            self.pointer = x
            self.skip_jump = True

    def op4(self, x: int):
        # bxc
        self.reg_b = self.reg_b ^ self.reg_c

    def op5(self, x: int):
        # out
        tmp = self.get_combo(x) % 8
        self.out += list(map(int, list(str(tmp))))

    def op6(self, x: int):
        # bdv
        tmp = self.adv_helper(x)
        self.reg_b = int(tmp)

    def op7(self, x: int):
        # cdv
        tmp = self.adv_helper(x)
        self.reg_c = int(tmp)


# Iterate over the linked list and apply splits
def parse_input(input: str) -> Computer:
    reg_a = re.findall(r"Register A: (\d+)", input)
    program = re.findall(r"Program: ([\d,*]+)", input)
    comp = Computer()

    comp.reg_a = int(reg_a[0])
    comp.reg_b = 0
    comp.reg_c = 0
    comp.program = list(map(int, program[0].split(",")))

    return comp


def run_all(input: str) -> str:
    comp = parse_input(input=input)

    out_list = comp.execute_program()
    out = ",".join(map(str, out_list))

    return out


import time

t0 = time.time()
input_path = "input/dec17.txt"
with open(input_path) as f:
    input = f.read()

val = run_all(input=input)

print(f"output: {val}")

t1 = time.time()
print(f"time: {(t1-t0)} seconds")


c = Computer()
c.reg_a = 117440
