from aocd.models import Puzzle
from aocd import submit
import os
from math import lcm
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    data = puzzle_input.split("\n")
    navigate, *lines = data
    maps = {l[0:3]: {'L': l[7:10], 'R': l[12:15]} for l in lines if l}
    return navigate, maps


def part1(data):
    """Solve part 1."""
    navigate, maps = data
    current = "AAA"
    for step, _ in enumerate(iter(int, 1)):
        if current == "ZZZ":
            break
        current = maps[current][navigate[step % len(navigate)]]
    return step


def part2(data):
    """Solve part 2."""
    navigate, maps = data
    currents = [{'origin': k, 'current': k, 'previous': []}
                for k in maps.keys() if k[2] == 'A']
    for step, _ in enumerate(iter(int, 1)):
        if all([k['current'][2] == 'Z' for k in currents]):
            break
        for node in currents:
            if node['current'][2] == 'Z':
                continue
            node['previous'].append(
                maps[node['current']][navigate[step % len(navigate)]])
            node['current'] = maps[node['current']
                                   ][navigate[step % len(navigate)]]

    return lcm(*[len(c['previous']) for c in currents])


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return f"{solution1}", f"{solution2}"


if __name__ == "__main__":
    for example in puzzle.examples:
        result_a, result_b = solve(example.input_data)
        if result_a != '2':
            print(f"Expected {example.answer_a}, got {result_a}")
            raise ValueError("Test case failed for Part A")

        if example.answer_b is not None:
            if result_b != '2':
                print(f"Expected {example.answer_b}, got {result_b}")
                raise ValueError("Test case failed for Part B")

    answer_a, answer_b = solve(puzzle.input_data)
    puzzle.answer_a = answer_a
    if answer_b != "None":
        puzzle.answer_b = answer_b
