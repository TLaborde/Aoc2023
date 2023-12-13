from aocd.models import Puzzle
from aocd import submit
import os

# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [line.split("\n") for line in puzzle_input.split("\n\n")]


def find_symetry(map):
    syms = 0
    for i in range(1, len(map)):
        if map[i-1] == map[i]:
            max_range = min(i-1, len(map)-1-i)
            sym = True
            for j in range(1, max_range+1):
                sym = sym and (map[i-j-1] == map[i+j])
            if sym:
                syms += i
    return syms


def almost_equal(a, b, smudge_fixed):
    if a == b:
        return smudge_fixed, True
    if smudge_fixed:
        return True, a == b
    else:
        if sum(1 for ca, cb in zip(a, b) if ca != cb) == 1:
            return True, True
        else:
            return False, False


def find_almost_symetry(map):
    syms = 0
    for i in range(1, len(map)):
        smudge_fixed = False
        smudge_fixed, mirror = almost_equal(map[i-1], map[i], smudge_fixed)
        if mirror:
            max_range = min(i-1, len(map)-1-i)
            sym = True
            for j in range(1, max_range+1):
                smudge_fixed, mirrored_line = almost_equal(
                    map[i-j-1], map[i+j], smudge_fixed)
                sym = sym and mirrored_line
            if sym and smudge_fixed:
                syms += i
    return syms


def transpose(matrix):
    return ["".join([str(matrix[i][j]) for i in range(len(matrix))]) for j in range(len(matrix[0]))]


def part1(data):
    """Solve part 1."""
    total = 0
    for map in data:
        total += find_symetry(map) * 100
        map = transpose(map)
        total += find_symetry(map)

    return total


def part2(data):
    """Solve part 2."""
    total = 0
    for map in data:
        total += find_almost_symetry(map) * 100
        map = transpose(map)
        total += find_almost_symetry(map)

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
