import os
import re
from aocd.models import Puzzle

# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split("\n")]


def part1(data):
    """Solve part 1."""
    total_sum = 0
    part_positions = {(i, match.start()) for i, line in enumerate(data) for match in re.finditer(r'[^\d|\.]', line)}
    for i, line in enumerate(data):
        matches = re.finditer(r'\d+', line)
        for match in matches:
            if any((y, x) in part_positions for x in range(match.start() - 1, match.end() + 1) for y in range(i - 1, i + 2)):
                total_sum += int(match.group())
    return total_sum


def part2(data):
    """Solve part 2."""
    gears = {}

    for i, line in enumerate(data):
        for match in re.finditer(r'\*', line):
            gears[(i, match.start())] = []

    for i, line in enumerate(data):
        for match in re.finditer(r'\d+', line):
            for x in range(match.start() - 1, match.end() + 1):
                for y in range(i - 1, i + 2):
                    if (y, x) in gears:
                        gears[(y, x)].append(int(match.group()))

    total_sum = sum(a * b for around in gears.values() if len(around) == 2 for a, b in [around])

    return total_sum


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
