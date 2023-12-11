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
    return [line for line in puzzle_input.split("\n")]


def transpose(matrix):
    return ["".join([str(matrix[i][j]) for i in range(len(matrix))]) for j in range(len(matrix[0]))]


def part1(data):
    """Solve part 1."""
    # This function is not used in the final code since part2 is the generalized case
    empty_lines = [i for i, line in enumerate(
        data) if re.fullmatch(r"\.+", line)]
    # we insert by the end, so we don't mess the indices for insert...
    for l in reversed(empty_lines):
        data.insert(l, data[l])
    data = transpose(data)
    empty_lines = [i for i, line in enumerate(
        data) if re.fullmatch(r"\.+", line)]
    for l in reversed(empty_lines):
        data.insert(l, data[l])
    data = transpose(data)
    galaxies = [(x, y) for x, line in enumerate(data)
                for y, cell in enumerate(line) if cell == "#"]
    pairs_dist = sum([abs(a[0]-b[0])+abs(a[1]-b[1]) for idx, a in enumerate(galaxies)
                      for b in galaxies[idx + 1:]])
    return pairs_dist


def part2(data, space_factor=1000000):
    """Solve part 2."""
    empty_lines = [i for i, line in enumerate(
        data) if re.fullmatch(r"\.+", line)]

    data_transposed = transpose(data)

    empty_rows = [i for i, line in enumerate(
        data_transposed) if re.fullmatch(r"\.+", line)]

    galaxies = [(x, y) for x, line in enumerate(data)
                for y, cell in enumerate(line) if cell == "#"]

    pairs_dist = sum(abs(a[0]-b[0]) + abs(a[1]-b[1]) +
                     (len([l for l in empty_rows if min(a[1], b[1]) < l < max(a[1], b[1])]) +
                      len([r for r in empty_lines if min(a[0], b[0]) < r < max(a[0], b[0])])) *
                     (space_factor - 1)
                     for i, a in enumerate(galaxies) for b in galaxies[i + 1:])
    return pairs_dist


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part2(data, 2)
    solution2 = part2(data)

    return f"{solution1}", f"{solution2}"


if __name__ == "__main__":
    for example in puzzle.examples:
        data = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
        result_a, result_b = solve(data)
        if result_a != example.answer_a:
            print(f"Expected {example.answer_a}, got {result_a}")
            raise ValueError("Test case failed for Part A")

        if example.answer_b is not None:
            if result_b != '82000210':
                print(f"Expected {example.answer_b}, got {result_b}")
                raise ValueError("Test case failed for Part B")

    answer_a, answer_b = solve(puzzle.input_data)
    puzzle.answer_a = answer_a
    if answer_b != "None":
        puzzle.answer_b = answer_b
