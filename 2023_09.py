from aocd.models import Puzzle
from aocd import submit
import os
from math import lcm
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [[int(i) for i in line.split()] for line in puzzle_input.split("\n")]

def solve_readings(readings, magic = -1):
    """ recurcive solve."""
    if any(readings):
        # calculate diff
        new_readings = [i - prev for prev, i in zip(readings, readings[1:])]
        return new_readings[magic] + (-2*magic-1) * solve_readings(new_readings, magic)
    else:
        return 0

def part1(data):
    """Solve part 1."""
    return sum(readings[-1] + solve_readings(readings) for readings in data)


def part2(data):
    """Solve part 2."""
    return sum(readings[0] - solve_readings(readings,0) for readings in data)


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
