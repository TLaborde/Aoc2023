from aocd.models import Puzzle
from aocd import submit
import os
from collections import defaultdict
import functools
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split(",")]


def get_hash(s):
    return functools.reduce(lambda h, c: ((h + ord(c)) * 17) % 256, s, 0)


def part1(data):
    """Solve part 1."""
    return sum(get_hash(step) for step in data)


def part2(data):
    """Solve part 2."""
    boxes = defaultdict(list)
    for step in data:
        if step[-1] == "-":
            label = step[:-1]
            hashed_label = get_hash(label)
            existing_lense = [
                l for l in boxes[hashed_label] if l[0] == label]
            if existing_lense:
                boxes[hashed_label].remove(existing_lense[0])
        else:
            label, focal_length = step.split("=")
            hashed_label = get_hash(label)
            existing_lense = [i for i, l in enumerate(
                boxes[hashed_label]) if l[0] == label]
            if existing_lense:
                boxes[hashed_label][existing_lense[0]][1] = int(focal_length)
            else:
                boxes[hashed_label].append([label, int(focal_length)])

    return sum((index+1) * (slot+1) *
               lense[1] for index, lenses in boxes.items() for slot, lense in enumerate(lenses))


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
