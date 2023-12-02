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


def part1(data):
    """Solve part 1."""
    sum = 0
    for line in data:
        game, subsets =line.split(":")
        subsets = subsets.split(";")
        possible = True
        for subset in subsets:
            cubes = subset.strip().split(",")
            for cube in cubes:
                number_cube, color_cube = cube.strip().split(" ")
                if color_cube == "red" and int(number_cube) > 12:
                    possible = False
                if color_cube == "green" and int(number_cube) > 13:
                    possible = False
                if color_cube == "blue" and int(number_cube) > 14:
                    possible = False
        if possible:
            sum =sum + int(game.split(" ")[1])
    return sum


def part2(data):
    """Solve part 2."""
    sum = 0
    for line in data:
        game, subsets =line.split(":")
        subsets = subsets.split(";")
        max_red = 0
        max_green = 0
        max_blue = 0
        for subset in subsets:
            cubes = subset.strip().split(",")
            for cube in cubes:
                number_cube, color_cube = cube.strip().split(" ")
                if color_cube == "red" and int(number_cube) > max_red:
                    max_red = int(number_cube)
                if color_cube == "green" and int(number_cube) > max_green:
                    max_green = int(number_cube)
                if color_cube == "blue" and int(number_cube) > max_blue:
                    max_blue= int(number_cube)
        sum =sum + max_red * max_blue * max_green
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
        if (example.answer_b):
           if answer_b != example.answer_b:
               print(f"expected {example.answer_b}, got {answer_b}")
               raise

    answer_a, answer_b = solve(puzzle.input_data)
    puzzle.answer_a = answer_a
    if answer_b != "None":
        puzzle.answer_b = answer_b
