from aocd.models import Puzzle
import os
from collections import deque
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    data = [line for line in puzzle_input.split("\n")]
    tables = {}
    tables_names = []
    _, rest = data[0].split(":")
    seeds = rest.split()
    for line in data[2:]:
        if len(line) <= 3:
            continue
        if ":" in line:
            category, _ = line.split(" ")
            tables_names.append(category)
            tables[category] = []
        else:
            tables[category].append([int(x) for x in line.split(" ")])
    return seeds, tables, tables_names


def table_to_value(table, value):
    return_val = value
    for entry in table:
        dest, source, count = entry
        if source <= value < source + count:
            return dest + (value - source)
    return return_val


def part1(data):
    """Solve part 1."""
    seeds, tables, table_names = data
    min_loc = float('inf')

    for seed in seeds:
        location = int(seed)
        for table_name in table_names:
            location = table_to_value(tables[table_name], location)
        min_loc = min(min_loc, location)

    return min_loc


def table_to_ranges(table, ranges):
    ranges = deque(ranges)
    return_val = []
    while ranges:
        range = ranges.popleft()
        for entry in table:
            dest, source, count = entry
            # all range included
            if source <= range[0] < source + count and source <= range[1] < source + count:
                return_val.append(
                    [dest - source + range[0], dest - source + range[1]])
                break
            if range[0] < source and range[1] >= source + count:
                return_val.append(
                    [dest, dest + count - 1])
                ranges.append([range[0], source - 1])
                ranges.append([source + count, range[1]])
                break
            # overlap
            if source <= range[0] < source + count:
                return_val.append(
                    [dest + (range[0] - source), dest + count - 1])
                ranges.append([source + count, range[1]])
                break
            # other overlap
            if source <= range[1] < source + count:
                return_val.append([dest, dest + (range[1] - source)])
                ranges.append([range[0], source - 1])
                break
        else:
            return_val.append(range)

    return return_val


def part2(data):
    """Solve part 2."""
    seeds, tables, table_names = data

    ranges = [[int(seeds[i]), int(seeds[i]) + int(seeds[i+1]) - 1]
              for i in range(0, len(seeds), 2)]

    for table_name in table_names:
        ranges = table_to_ranges(tables[table_name], ranges)

    return min(r[0] for r in ranges)


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
