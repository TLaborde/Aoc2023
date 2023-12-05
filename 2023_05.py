from aocd.models import Puzzle
from aocd import submit
import os
from collections import deque
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split("\n")]


def table_to_value(table, value):
    return_val = value
    for entry in table:
        dest, source, count = entry
        if source <= value < source + count:
            return dest + (value - source)
    return return_val


def part1(data):
    """Solve part 1."""
    tables = {}
    _, rest = data[0].split(":")
    seeds = rest.split()
    for line in data[2:]:
        if len(line) <= 3:
            continue
        if ":" in line:
            category, _ = line.split(" ")
            tables[category] = []
        else:
            tables[category].append([int(x) for x in line.split(" ")])
    min_loc = None

    for seed in seeds:
        soil = table_to_value(tables['seed-to-soil'], int(seed))
        fertilizer = table_to_value(tables['soil-to-fertilizer'], soil)
        water = table_to_value(tables['fertilizer-to-water'], fertilizer)
        light = table_to_value(tables['water-to-light'], water)
        temperature = table_to_value(tables['light-to-temperature'], light)
        humidity = table_to_value(
            tables['temperature-to-humidity'], temperature)
        location = table_to_value(tables['humidity-to-location'], humidity)

        if not min_loc or min_loc > location:
            min_loc = location

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

    print(count_range(return_val))
    return return_val


def part2(data):
    """Solve part 2."""
    tables = {}
    _, rest = data[0].split(":")
    seeds = rest.split()
    for line in data[2:]:
        if len(line) <= 3:
            continue
        if ":" in line:
            category, _ = line.split(" ")
            tables[category] = []
        else:
            tables[category].append([int(x) for x in line.split(" ")])

    min_loc = None
    ranges = []
    for i in range(int(len(seeds)/2)):
        ranges.append(
            [int(seeds[i*2]), int(seeds[i*2]) + int(seeds[2*i+1]) - 1])

    ranges = table_to_ranges(tables['seed-to-soil'], ranges)
    ranges = table_to_ranges(tables['soil-to-fertilizer'], ranges)
    ranges = table_to_ranges(tables['fertilizer-to-water'], ranges)
    ranges = table_to_ranges(tables['water-to-light'], ranges)
    ranges = table_to_ranges(tables['light-to-temperature'], ranges)
    ranges = table_to_ranges(tables['temperature-to-humidity'], ranges)
    ranges = table_to_ranges(tables['humidity-to-location'], ranges)

    for r in ranges:
        if not min_loc or min_loc > r[0]:
            min_loc = r[0]

    return min_loc


def count_range(ranges):
    sum = 0
    for r in ranges:
        sum += r[1]-r[0] + 1
    return sum


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return f"{solution1}", f"{solution2}"


def test_table_to_ranges():
    table = [
        [100, 10, 5]
    ]
    ranges = [[1, 20]]
    expected_output = [[100, 104], [1, 9], [15, 20]]
    result = table_to_ranges(table, ranges)
    assert result == expected_output

    table = [
        [100, 10, 5]
    ]
    ranges = [[11, 20]]
    expected_output = [[101, 104], [15, 20]]
    result = table_to_ranges(table, ranges)
    assert result == expected_output

    table = [
        [100, 10, 5]
    ]
    ranges = [[11, 12]]
    expected_output = [[101, 102]]
    result = table_to_ranges(table, ranges)
    assert result == expected_output

    table = [
        [100, 10, 5]
    ]
    ranges = [[1, 12]]
    expected_output = [[100, 102], [1, 9]]
    result = table_to_ranges(table, ranges)
    assert result == expected_output

    table = [
        [100, 10, 5]
    ]
    ranges = [[1, 12], [13, 20]]
    expected_output = [[100, 102], [103, 104], [1, 9], [15, 20]]
    result = table_to_ranges(table, ranges)
    assert result == expected_output


if __name__ == "__main__":
    test_table_to_ranges()

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
