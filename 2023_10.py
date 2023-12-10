from aocd.models import Puzzle
from aocd import submit
import os
from collections import defaultdict
import re
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    data = [list(line) for line in puzzle_input.split("\n")]

    mapping = defaultdict(list)
    start = None

    for x, line in enumerate(data):
        for y, cell in enumerate(line):
            if cell in "|-LJ7FS":
                mapping[(x, y)] = [(x + dx, y + dy) for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0))]

                if cell == "|":
                    mapping[(x, y)] = [(x - 1, y), (x + 1, y)]
                elif cell == "-":
                    mapping[(x, y)] = [(x, y - 1), (x, y + 1)]
                elif cell == "L":
                    mapping[(x, y)] = [(x - 1, y), (x, y + 1)]
                elif cell == "J":
                    mapping[(x, y)] = [(x - 1, y), (x, y - 1)]
                elif cell == "7":
                    mapping[(x, y)] = [(x, y - 1), (x + 1, y)]
                elif cell == "F":
                    mapping[(x, y)] = [(x, y + 1), (x + 1, y)]
                elif cell == "S":
                    start = (x, y)

    path = [start]
    neighbours = mapping[start]

    while neighbours:
        path.extend(neighbours)
        neighbours = [i for n in neighbours for i in mapping[n] if i not in path]

    return data, path


def part1(data):
    """Solve part 1."""
    data, path = data
    return int((len(path)-2)/2)


def part2(data):
    """Solve part 2."""
    _, path = data  # Unpack only the necessary variable

    # Clean the map
    data = [
        [cell if (x, y) in path else "." for y, cell in enumerate(line)]
        for x, line in enumerate(data)
    ]

    outside_cells= 0
    for line in data:
        inside = False
        # replace any north/south with normal pipe, ignore u-bend
        line = re.sub(r"F-*J|L-*7", "|", "".join(line))
        for cell in line:
            if cell == "|":
                inside = not inside
            if inside and cell == ".":
                outside_cells += 1
    return outside_cells       
    


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return f"{solution1}", f"{solution2}"


if __name__ == "__main__":
    for example in puzzle.examples:
        data="""..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""
        result_a, result_b = solve(data)
        if result_a != '8':
            print(f"Expected {example.answer_a}, got {result_a}")
            raise ValueError("Test case failed for Part A")
        data = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""
        result_a, result_b = solve(data)
        if example.answer_b is not None:
            if result_b != example.answer_b:
                print(f"Expected {example.answer_b}, got {result_b}")
                raise ValueError("Test case failed for Part B")

    answer_a, answer_b = solve(puzzle.input_data)
    puzzle.answer_a = answer_a
    if answer_b != "None":
        puzzle.answer_b = answer_b
