from aocd.models import Puzzle
from aocd import submit
import os
import time
from math import sqrt, ceil, floor
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    data = [line for line in puzzle_input.split("\n")]
    times = list(map(int, data[0].split()[1:]))
    distances = list(map(int, data[1].split()[1:]))
    return times, distances


def part1(data):
    """Solve part 1."""
    times, distances = data
    total = 1
    for i, time in enumerate(times):
        sol = floor(1+(- time + sqrt(time*time - 4 * (-1)
                                     * (- distances[i]))) / (2 * -1))
        total *= (time - 2 * sol + 1)
    return total


def part2(data):
    times, distances = data
    time = int("".join(map(str, times)))
    d = int("".join(map(str, distances)))
    # -j * 2 + time * j - distance = 0
    sol = ceil((- time + sqrt(time*time - 4 * (-1) * (- d))) / (2 * -1))
    return (time - sol*2 + 1)


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    start_time = time.time()

    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    end_time = time.time()
    time_taken = end_time - start_time

    print(f"Time taken to solve the puzzle: {time_taken:.6f} seconds")
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
