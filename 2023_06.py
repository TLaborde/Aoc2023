from aocd.models import Puzzle
from aocd import submit
import os

# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split("\n")]


def part1(data):
    """Solve part 1."""
    times = [int(x) for x in data[0].split()[1::]]
    distances = [int(x) for x in data[1].split()[1::]]
    total = 1
    for i, time in enumerate(times):
        for j in range(time):
            distance = j * (time-j)
            if distance > distances[i]:
                min_push = j
        for j in reversed(range(time)):
            distance = j * (time-j)
            if distance > distances[i]:
                max_push = j
        total *= (min_push - max_push + 1)
    return total


def part2(data):
    time = int("".join(data[0].split()[1::]))
    d = int("".join(data[1].split()[1::]))
    total = 1
    min_push = 0
    max_push = 0
    for j in range(time):
        distance = j * (time-j)
        if distance > d:
            min_push = j
    for j in reversed(range(time)):
        distance = j * (time-j)
        if distance > d:
            max_push = j
    total *= (min_push - max_push + 1)
    return total


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return f"{solution1}", f"{solution2}"


if __name__ == "__main__":
    for example in puzzle.examples:
        result_a, result_b = solve(example.input_data)
        if result_a != '288':
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
