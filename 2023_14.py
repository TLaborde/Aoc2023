from aocd.models import Puzzle
from aocd import submit
import os

# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split()]


def transpose(matrix):
    return ["".join([str(matrix[i][j]) for i in range(len(matrix))]) for j in range(len(matrix[0]))]


def calculate_weight(data):
    """Solve part 1."""
    rows = transpose(data)
    total_weight = 0
    for row in rows:
        row = list(row)
        for i, cell in enumerate(row):
            if cell == "O":
                total_weight += len(row) - i

    return total_weight


def part1(data):
    """Solve part 1."""
    rows = transpose(data)
    total_weight = 0
    for row in rows:
        row = list(row)
        for i, cell in enumerate(row):
            if cell == "#":
                continue
            if cell == "O":
                j = i - 1
                while j >= 0 and row[j] == ".":
                    row[j], row[j+1] = row[j+1], row[j]
                    j -= 1
        for i, cell in enumerate(row):
            if cell == "O":
                total_weight += len(row) - i

    return total_weight


def m_transpose(matrix):
    return [[str(matrix[i][j]) for i in range(len(matrix))] for j in range(len(matrix[0]))]


def roll(data):
    for row in data:
        for i, cell in enumerate(row):
            if cell == "#":
                continue
            if cell == "O":
                j = i - 1
                while j >= 0 and row[j] == ".":
                    row[j], row[j+1] = row[j+1], row[j]
                    j -= 1
    return data


def do_cycle(data):
    north = m_transpose(data)
    north = roll(north)
    north = m_transpose(north)
    west = roll(north)
    south = list(reversed(west))
    south = m_transpose(south)
    south = roll(south)
    south = m_transpose(south)
    south = list(reversed(south))
    east = [list(reversed(r)) for r in south]
    east = roll(east)
    east = [list(reversed(r)) for r in east]
    return east

    return data


def part2(data):
    """Solve part 2."""
    data = [[c for c in l] for l in data]
    previous = list()
    result = ""
    for i in range(1000000000):
        data = do_cycle(data)
        result = "".join(cell for row in data for cell in row)
        if result in previous:
            break
        else:
            previous.append(result)
    index = previous.index(result)
    cycle_length = len(previous) - index
    final_index = ((1000000000 - index) % cycle_length) + index - 1
    print(previous[final_index])
    print(len(previous), index, final_index)
    s = previous[final_index]
    s = [s[i:i + len(data[0])] for i in range(0, len(s), len(data[0]))]

    weight = calculate_weight(s)
    return weight


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
            if result_b != "64":
                print(f"Expected 64, got {result_b}")
                raise ValueError("Test case failed for Part B")

    answer_a, answer_b = solve(puzzle.input_data)
    puzzle.answer_a = answer_a
    if answer_b != "None":
        puzzle.answer_b = answer_b
