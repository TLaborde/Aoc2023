from aocd.models import Puzzle
from aocd import submit
import os
import re
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split()]


def f_A(x, m, a, s):
    return True


def f_R(x, m, a, s):
    return False


def part1(data):
    """Solve part 1."""
    functions = [line for line in data if line[0] not in ["{", ""]]
    inputs = [line for line in data if line[0] == "{"]

    to_run = """
def f_A(x, m, a, s):
    return True

def f_R(x, m, a, s):
    return False

"""
    for f in functions:
        name, steps = f.split("{")
        to_run += "def f_" + name + "(x,m,a,s):\r\n"
        steps = steps[:-1].split(",")
        for s in steps:
            if ":" in s:
                cond, act = s.split(":")
                to_run += f"""
    if {cond}:
        return f_{act}(x,m,a,s)
"""
            else:
                to_run += f"""
    return f_{s}(x,m,a,s)
"""

    # don't do this at home kids
    exec(to_run, globals())

    total = 0
    for i in inputs:
        input_val = [int(s) for s in re.findall(r'\d+', i)]
        if f_in(*input_val):
            total += sum(input_val)
    return total


def part2(data):
    """Solve part 1."""
    functions = [line for line in data if line[0] not in ["{", ""]]
    inputs = [line for line in data if line[0] == "{"]

    to_run = """
def f_A(x, m, a, s):
    return (x[1]-x[0] + 1) * (m[1]-m[0] + 1) * (a[1]-a[0] + 1) * (s[1]-s[0] + 1)

def f_R(x, m, a, s):
    return 0

"""
    for f in functions:
        name, steps = f.split("{")
        to_run += f"""
def f_{name}(x,m,a,s):
    return_val = 0
"""
        for s in steps[:-1].split(","):
            if ":" in s:
                cond, act = s.split(":")
                var = cond[0]
                op = cond[1]
                number = cond[2:]
                to_run += f"""
    r = split_range ({var}, '{op}', {number})
    if r[0]:
        {var} = r[0]
        return_val += f_{act}(x, m, a, s)
    {var} = r[1]
"""
            else:
                to_run += f"""
    return_val += f_{s}(x, m, a, s)
    return return_val
"""
    exec(to_run, globals())

    total = f_in([1, 4000], [1, 4000], [1, 4000], [1, 4000])
    return total


def split_range(r, op, val):
    # 200 > s
    if op == "<":
        if r[0] < val < r[1]:
            return [[r[0], val-1], [val, r[1]]]
        if val > r[1]:
            return [r, []]
        if val < r[0]:
            return [[], r]
    else:
        # 200 < range
        if r[0] < val < r[1]:
            return [[val+1, r[1]], [r[0], val]]
        if val > r[1]:
            return [[], r]
        if val < r[0]:
            return [r, []]


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return f"{solution1}", f"{solution2}"


if __name__ == "__main__":
    for example in puzzle.examples:
        result_a, result_b = solve(example.input_data)
        if result_a != example.answer_a:
            print(f"Expected {example.answer_a}, got {result_a}")
            raise ValueError("Test case failed for Part A")

        if example.answer_b is not None:
            if result_b != example.answer_b:
                print(f"Expected {example.answer_b}, got {result_b}")
                raise ValueError("Test case failed for Part B")

    answer_a, answer_b = solve(puzzle.input_data)
    puzzle.answer_a = answer_a
    if answer_b != "None":
        puzzle.answer_b = answer_b
