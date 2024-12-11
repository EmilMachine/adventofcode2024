# Implement splitting rules and apply them itterative over all elements
# It seems maybe a linked list structure would be nice to handle all the splitting in middle of list
# Note: order doesn't matter see b for iterative approach with dictionary memorization
import numpy as np


def split_int(a: int) -> tuple[int, int]:
    length = np.ceil(np.log10(a + 1))
    zeros = 10 ** (length / 2)
    left = a // zeros
    right = a - zeros * left
    return int(left), int(right)


def mutate(val: int) -> tuple[int]:
    if val == 0:
        return (1,)
    length = np.ceil(np.log10(val + 1)) % 2 == 0
    if length:
        return split_int(a=val)
    return (val * 2024,)


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.len = 0

    def append(self, value):
        if not self.head:
            self.head = Node(value)
            self.len = 1
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = Node(value)
            self.len += 1

    def __iter__(self):
        self.current = self.head
        return self

    def __next__(self):
        if not self.current:
            raise StopIteration
        value = self.current.value
        self.current = self.current.next
        return value

    def mutate_iter(self):
        current = self.head
        previous = None

        while current:
            tmp_val = mutate(current.value)
            if len(tmp_val) == 1:
                current.value = tmp_val[0]
            else:
                new_node1 = Node(tmp_val[0])
                new_node2 = Node(tmp_val[1])

                new_node2.next = current.next
                new_node1.next = new_node2

                if previous:
                    previous.next = new_node1
                else:
                    self.head = new_node1

                current = new_node2
                self.len += 1

            previous = current
            current = current.next

    def print_list(self):
        current = self.head
        while current:
            print(current.value, end=" ")
            current = current.next
        print()


# Iterate over the linked list and apply splits
def parse_input(input: str) -> LinkedList:
    linkedlist = LinkedList()
    for i in input.split(" "):
        linkedlist.append(int(i))
    return linkedlist


def run_all(input: str) -> list[int]:
    linkedlist = parse_input(input=input)

    n_blinks = 25
    for _ in range(n_blinks):
        linkedlist.mutate_iter()
    return linkedlist.len


import time

t0 = time.time()
input_path = "input/dec11.txt"

with open(input_path) as f:
    input = f.read()


val = run_all(input=input)

print(f"n stones: {val}")

t1 = time.time()
print(f"time: {(t1-t0)} secunds")
