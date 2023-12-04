from aocd.models import Puzzle
from aocd import submit
import os
import re
from collections import defaultdict
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split("\n")]


def part1(data):
    """Solve part 1."""
    total_winnings = 0
    for line in data:
        _, winning_numbers, numbers_i_have = re.split(r'\||:', line)
        common_numbers_count = len(set(winning_numbers.split()).intersection(
            set(numbers_i_have.split())))
        if common_numbers_count:
            total_winnings += 2 ** (common_numbers_count - 1)
    return total_winnings


def part2(data):
    """Solve part 2."""
    copies = {i: 1 for i in range(1, len(data)+1)}
    for i, line in enumerate(data):
        _, winning_numbers, numbers_i_have = re.split(r'\||:', line)
        copy_count = len(set(winning_numbers.split()).intersection(
            set(numbers_i_have.split())))
        if copy_count:
            for c in range(copy_count):
                copies[i+2+c] += copies[i+1]
    return sum(copies.values())


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
