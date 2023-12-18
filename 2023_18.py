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


def is_valid(n, min_x, max_x, min_y, max_y):
    return min_x <= n[0] <= max_x and min_y <= n[1] <= max_y


def part1(data):
    """Solve part 1."""
    grid = [(0, 0)]
    for line in data:
        direction, distance, color = line.split()
        last = grid[-1]
        if direction == 'R':
            for i in range(int(distance)):
                grid.append((last[0] + 1 + i, last[1]))
        if direction == 'L':
            for i in range(int(distance)):
                grid.append((last[0] - 1 - i, last[1]))
        if direction == 'D':
            for i in range(int(distance)):
                grid.append((last[0], last[1] + 1 + i))
        if direction == 'U':
            for i in range(int(distance)):
                grid.append((last[0], last[1] - 1 - i))
    min_x = min(c[0] for c in grid)
    max_x = max(c[0] for c in grid)
    min_y = min(c[1] for c in grid)
    max_y = max(c[1] for c in grid)

    # need to do a flood fill from all external side
    outside = set()
    to_check = deque()
    for j in range(min_y, max_y+1):
        if (min_x, j) not in grid:
            to_check.append((min_x, j))
        if (max_x, j) not in grid:
            to_check.append((max_x, j))
    for i in range(min_x+1, max_x):
        if (i, min_y)not in grid:
            to_check.append((i, min_y))
        if (i, max_y)not in grid:
            to_check.append((i, max_y))
    while to_check:
        print(len(to_check))
        coords = to_check.pop()
        outside.add(coords)

        neighbours = [(coords[0]-1, coords[1]), (coords[0]+1, coords[1]),
                      (coords[0], coords[1]-1), (coords[0], coords[1]+1)]
        for n in neighbours:
            if is_valid(n, min_x, max_x, min_y, max_y) and n not in to_check and n not in grid and n not in outside:
                to_check.append(n)
    return (max_x-min_x+1)*(max_y-min_y+1) - len(outside)


def intersect(point, lines):
    return any((x1 == point[0] and min(y1, y2) <= point[1] <= max(y1, y2)) or (y1 == point[1] and min(y1, y2) <= point[1] <= max(y1, y2)) for (x1, y1, x2, y2) in lines)


def part2(data):
    """Solve part 2."""
    start = (0, 0)  # x1,y1,x2,y2
    perimeter = [start]
    for line in data:
        _, _, color = line.split()
        digitToColor = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
        direction = digitToColor[color[-2]]
        distance = int(color[2:7], 16)
        last = perimeter[-1]
        if direction == 'R':
            perimeter.append((last[0] + int(distance), last[1]))
        if direction == 'L':
            perimeter.append((last[0] - int(distance), last[1]))
        if direction == 'D':
            perimeter.append((last[0], last[1] + int(distance)))
        if direction == 'U':
            perimeter.append((last[0], last[1] - int(distance)))

    all_x = sorted(set(p[0] for p in perimeter))
    all_y = sorted(set(p[1] for p in perimeter))
    x_lenghts = [1]
    for i, x in enumerate(all_x[1:]):
        x_lenghts.extend([x-all_x[i]-1, 1])
    y_lengths = [1]
    for j, y in enumerate(all_y[1:]):
        y_lengths.extend([y-all_y[j]-1, 1])
    area = {}
    for i, x in enumerate(x_lenghts):
        for j, y in enumerate(y_lengths):
            area[(i, j)] = x*y

    big_to_small = {}
    for i, x in enumerate(all_x):
        for j, y in enumerate(all_y):
            big_to_small[(x, y)] = (2*i, 2*j)
    grid = [(0, 0)]
    for l, line in enumerate(data):
        _, _, color = line.split()
        digitToColor = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
        direction = digitToColor[color[-2]]
        distance = int(color[2:7], 16)
        last = grid[-1]
        next = big_to_small[perimeter[l+1]]

        if direction == 'R':
            distance = next[0] - last[0]
            for i in range(distance):
                grid.append((last[0] + 1 + i, last[1]))
        if direction == 'L':
            distance = next[0] - last[0]
            for i in range(-distance):
                grid.append((last[0] - 1 - i, last[1]))
        if direction == 'D':
            distance = next[1] - last[1]
            for i in range(int(distance)):
                grid.append((last[0], last[1] + 1 + i))
        if direction == 'U':
            distance = next[1] - last[1]
            for i in range(-distance):
                grid.append((last[0], last[1] - 1 - i))

    min_x = min(c[0] for c in grid)
    max_x = max(c[0] for c in grid)
    min_y = min(c[1] for c in grid)
    max_y = max(c[1] for c in grid)

    # need to do a flood fill from all external side
    outside = set()
    to_check = deque()
    for j in range(min_y, max_y+1):
        if (min_x, j) not in grid:
            to_check.append((min_x, j))
        if (max_x, j) not in grid:
            to_check.append((max_x, j))
    for i in range(min_x+1, max_x):
        if (i, min_y)not in grid:
            to_check.append((i, min_y))
        if (i, max_y)not in grid:
            to_check.append((i, max_y))
    while to_check:
        print(len(to_check))
        coords = to_check.pop()
        outside.add(coords)

        neighbours = [(coords[0]-1, coords[1]), (coords[0]+1, coords[1]),
                      (coords[0], coords[1]-1), (coords[0], coords[1]+1)]
        for n in neighbours:
            if is_valid(n, min_x, max_x, min_y, max_y) and n not in to_check and n not in grid and n not in outside:
                to_check.append(n)
    outside_area = sum(area[box] for box in outside)
    total_area = (all_x[-1] - all_x[0] + 1) * (all_y[-1] - all_y[0] + 1)
    result = total_area - outside_area
    return total_area - outside_area


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = None  # part1(data)
    solution2 = part2(data)

    return f"{solution1}", f"{solution2}"


if __name__ == "__main__":
    for example in puzzle.examples:
        result_a, result_b = solve(example.input_data)
        # if result_a != example.answer_a:
        #    print(f"Expected {example.answer_a}, got {result_a}")
        #    raise ValueError("Test case failed for Part A")

        if example.answer_b is not None:
            if result_b != example.answer_b:
                print(f"Expected {example.answer_b}, got {result_b}")
                raise ValueError("Test case failed for Part B")

    answer_a, answer_b = solve(puzzle.input_data)
    # puzzle.answer_a = answer_a
    if answer_b != "None":
        puzzle.answer_b = answer_b
