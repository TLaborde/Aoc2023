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


def part1(data):
    """Solve part 1."""
    sum = 0
    for line in data:
        numbers = re.findall(r'\d', line)
        sum = sum + int(numbers[0])*10 + int(numbers[-1])
    return sum


def part2(data):
    """Solve part 2."""
    sum = 0
    table = {
        # 'zero': 0,
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        '0': 0,
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9
    }
    for line in data:
        numbers = re.findall(
            r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))", line)
        if numbers[0] == '0':
            print(table[numbers[0]])
        if numbers[-1] == '0':
            print(table[numbers[-1]])
        sum = sum + table[numbers[0]]*10 + table[numbers[-1]]
    print(sum)
    return sum


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return f"{solution1}", f"{solution2}"


if __name__ == "__main__":
    for example in puzzle.examples:
        answer_a, answer_b = solve(example.input_data)
        if answer_a != example.answer_a:
            print(f"expected {example.answer_a}, got {answer_a}")
            raise
        # if (example.answer_b):
        #    if answer_b != example.answer_b:
        #        print(f"expected {example.answer_b}, got {answer_b}")
        #        raise

    answer_a, answer_b = solve(puzzle.input_data)
    puzzle.answer_a = answer_a
    if answer_b != "None":
        puzzle.answer_b = answer_b
