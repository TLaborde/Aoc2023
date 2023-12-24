from aocd.models import Puzzle
from aocd import submit
import os
from collections import deque, defaultdict
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))

class Module:
    def __init__(self, line):
        type, dests = line.split(" -> ")
        if type[0] == "&":
            self.type = "conj"
            self.name = type[1:]
            self.memory = {}

        elif type[0] == "%":
            self.type = "ff"
            self.name = type[1:]
            self.state = False

        else:
            self.type = "special"
            self.name = type

        self.dests = dests.split(", ")       
    def process_conj(self, pulse, source):
        self.memory[source] = pulse
        if all(self.memory.values()):
            return Pulse.LOW
        else:
            return Pulse.HIGH  
    def process_ff(self,  pulse, source=""):
        if pulse == Pulse.LOW:
            self.state = not self.state
            if self.state:
                return Pulse.HIGH
            else:
                return Pulse.LOW
        else:
            return None
    def process(self,  pulse, source=""):
        if self.type == "conj":
            return self.process_conj(pulse, source)
        elif self.type == "ff":
            return self.process_ff(pulse,source)
        else:
            return pulse

from enum import Flag

class Pulse(Flag):
    HIGH = True
    LOW = False

class State(Flag):
    OFF = False
    ON = True

def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split("\n")]


def part1(data):
    """Solve part 1."""
    machine = {}
    for line in data:
        m = Module(line)
        machine[m.name] = m
    # setup
    all_valls = list(machine.values())
    for m in all_valls:
        for n in m.dests:
            if n not in machine:
                machine[n] = Module(n + " -> ")
            if machine[n].type == "conj":
                machine[n].memory[m.name] = Pulse.LOW
    actions = deque()
    high_count = 0
    low_count = 0
    for _ in range(1000):
        actions.append(("button","broadcaster",Pulse.LOW))
        while actions:
            source, target, pulse = actions.popleft()
            if pulse == Pulse.HIGH:
                high_count +=1
            else:
                low_count += 1
            res = machine[target].process(pulse,source)
            if res != None:
                for n in machine[target].dests :
                    if n != '':
                        actions.append((target, n, res))
    return high_count * low_count


def part2(data):
    """Solve part 1."""
    machine = {}
    for line in data:
        m = Module(line)
        machine[m.name] = m
    # setup
    all_valls = list(machine.values())
    for m in all_valls:
        for n in m.dests:
            if n not in machine:
                machine[n] = Module(n + " -> ")
            if machine[n].type == "conj":
                machine[n].memory[m.name] = Pulse.LOW
    actions = deque()
    p_count = 0
    if "rx" not in machine:
        return 1
    while True:
        actions.append(("button","broadcaster",Pulse.LOW))
        rx = 0
        p_count += 1
        while actions:
            source, target, pulse = actions.popleft()
            if target == "rx" and pulse == Pulse.LOW:
                rx += 1
            res = machine[target].process(pulse,source)
            if res != None:
                for n in machine[target].dests :
                    if n != '':

                        actions.append((target, n, res))
        if rx >= 1:
            print(rx)
            print(p_count)
            return p_count
        


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return f"{solution1}", f"{solution2}"


if __name__ == "__main__":
    for example in puzzle.examples:
        result_a, result_b = solve(example.input_data)
        if result_a != '32000000':
            print(f"Expected {example.answer_a}, got {result_a}")
            raise ValueError("Test case failed for Part A")

        #if example.answer_b is not None:
        #    if result_b != example.answer_b:
        #        print(f"Expected {example.answer_b}, got {result_b}")
        #        raise ValueError("Test case failed for Part B")

    answer_a, answer_b = solve(puzzle.input_data)
    puzzle.answer_a = answer_a
    if answer_b != "None":
        puzzle.answer_b = answer_b
