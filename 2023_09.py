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
    data = puzzle_input.split("\n")
    return data

def solve_readings(readings):
    if any(readings):
        # calculate diff
        prev = readings[0]
        b = [ ]
        for i in readings[1:]:
            b.append(i - prev)
            prev = i
        return b[-1] + solve_readings(b)
    else:
        return 0

def solve_readings2(readings):
    print(readings)
    if any(readings):
        prev = readings[0]
        b = [ ]
        for i in readings[1:]:
            b.append(i - prev)
            prev = i

        return b[0] - solve_readings2(b)
    else:
        return 0

def part1(data):
    """Solve part 1."""
    sum = 0
    for line in data:
        readings = [int(i) for i in line.split(" ")]
        sum += readings[-1] + solve_readings(readings)
    return sum


def part2(data):
    """Solve part 2."""
    sum = 0
    for line in data:
        readings = [int(i) for i in line.split(" ")]
        sum += readings[0] - solve_readings2(readings)
        print(readings[0] - solve_readings2(readings))
    return sum


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
