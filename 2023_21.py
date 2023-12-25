from aocd.models import Puzzle
from aocd import submit
import os

# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [[c for c in line ]for line in puzzle_input.split()]

def get_nei(points, map):
    nei = set()
    for (x,y) in points:
        x +=1
        if x < len(map) and map[x][y] == '.' and (x,y) not in nei:
            nei.add((x,y))
        x -= 2
        if x >= 0 and map[x][y] == '.' and (x,y) not in nei:
            nei.add((x,y))
        x +=1
        y += 1
        if y < len(map[0]) and map[x][y] == '.' and (x,y) not in nei:
            nei.add((x,y))
        y -= 2
        if y >= 0 and map[x][y] == '.' and (x,y) not in nei:
            nei.add((x,y))
    return nei

def get_infinite_nei(points, map):
    nei = set()
    for (x,y) in points:
        x +=1
        if map[x%len(map)][y%len(map[0])] in ['.','S'] and (x,y) not in nei:
            nei.add((x,y))
        x -= 2
        if map[x%len(map)][y%len(map[0])] in ['.','S'] and (x,y) not in nei:
            nei.add((x,y))
        x +=1
        y += 1
        if map[x%len(map)][y%len(map[0])] in ['.','S'] and (x,y) not in nei:
            nei.add((x,y))
        y -= 2
        if map[x%len(map)][y%len(map[0])] in ['.','S'] and (x,y) not in nei:
            nei.add((x,y))
    return nei

def part1(data):
    knowns = set()
    to_discover = set()
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            if c == "S":
                to_discover.add((i,j))
    if len(data) == 11:
        r = 3
    else:
        r = 32
    for _ in range(r):
        nei = get_nei(get_nei(to_discover, data),data)
        to_discover = [n for n in nei if n not in knowns] 
        for t in nei:
            if t not in knowns:
                knowns.add(t)
    return len(knowns)+1

def reachable(data, r):
    knowns = set()
    to_discover = set()
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            if c == "S":
                to_discover.add((i,j))

    for _ in range(r):
        nei = get_infinite_nei(to_discover, data)
        to_discover = [n for n in nei if n not in knowns] 
        for t in nei:
            if t not in knowns:
                knowns.add(t)
    knowns = [(x,y) for (x,y) in knowns if (x +y)% 2 == r %2 ]
    return len(knowns)

def part2(data):
    if len(data) == 11:
        steps = [6,10,50,100,500]
    else:
        steps = [65+ 131, 65+ 131*2, 65+ 131*3]

    plots = [reachable(data, s) for s in steps]

    print(plots)
    import numpy as np
    # hours = [6, 10,50,100,500,1000,5000]
    # happ = [16,50,1594,6536,167004,668697,16733044]
    # #polynomial fit with degree = 2
    model = np.poly1d(np.polyfit(steps, plots, 2))
    print(model)
    # #add fitted polynomial line to scatterplot
    print(model(26501365))
    return int(model(26501365))


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return f"{solution1}", f"{solution2}"


if __name__ == "__main__":
    for example in puzzle.examples:
        result_a, result_b = solve(example.input_data)
        if result_a != '16':
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
