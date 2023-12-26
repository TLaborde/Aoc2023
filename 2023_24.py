from aocd.models import Puzzle
from aocd import submit
import os
from itertools import combinations

import z3
import numpy as np
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [[tuple(map(int,coord.split(", "))) for coord in line.split("@")]  for line in puzzle_input.split("\n") ]

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def get_2p(p):
    return [[p[0][0],p[0][1]],[p[0][0]+p[1][0],p[0][1]+p[1][1]]]

def intersect_right_dir(intersec,p):
    return (p[1][0] > 0 and intersec[0]> p[0][0]) or (p[1][0] < 0 and intersec[0]< p[0][0]) 


def part1(data):
    """Solve part 1."""
    if len(data) == 5:
        coord_min = 7
        coord_max = 27
    else:
        coord_min = 200000000000000
        coord_max = 400000000000000
    result = 0
    for p1,p2 in combinations(data,2):
        p1c = get_2p(p1)
        p2c = get_2p(p2)
        if p1 !=p2:
            #print("Hailstone A:", p1)
            #print("Hailstone B:", p2)
            intersec = line_intersection(p1c,p2c)
            if intersec == None:
                pass
                #print("Hailstones' paths are parallel; they never intersect.")
            else:
                if not intersect_right_dir(intersec,p1) or not intersect_right_dir(intersec,p2):
                    #print("Hailstones' paths crossed in the past for both hailstones.")
                    pass
                elif coord_min <= intersec[0] <= coord_max and coord_min <= intersec[1] <= coord_max:
                    #print(f"Hailstones' paths will cross inside the test area (at x={intersec[0]}, y={intersec[1]}).")
                    result += 1
                else:
                    pass
                    #print(f"Hailstones' paths will cross outside the test area (at x={intersec[0]}, y={intersec[1]}).")
    return result


def part2(data):
    # we use a solver for the equations, ain't nobody got time to do that manually
    t1, t2, t3, x, y, z, vx, vy, vz = z3.Reals("t1 t2 t3 x y z vx vy vz")
    (A0x, A0y, A0z), (V0x, V0y, V0z) = data[0]
    (A1x, A1y, A1z), (V1x, V1y, V1z) = data[1]
    (A2x, A2y, A2z), (V2x, V2y, V2z) = data[2]
    equations = [
        x + t1 * vx == A0x + t1 * V0x,
        y + t1 * vy == A0y + t1 * V0y,
        z + t1 * vz == A0z + t1 * V0z,
        x + t2 * vx == A1x + t2 * V1x,
        y + t2 * vy == A1y + t2 * V1y,
        z + t2 * vz == A1z + t2 * V1z,
        x + t3 * vx == A2x + t3 * V2x,
        y + t3 * vy == A2y + t3 * V2y,
        z + t3 * vz == A2z + t3 * V2z,
    ]
    s = z3.Solver()
    s.add(*equations)
    s.check()
    r = s.model()
    coord = [r[coord].as_long() for coord in [x, y, z]]
    return sum(coord)


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
            if result_b != example.answer_b:
                print(f"Expected {example.answer_b}, got {result_b}")
                raise ValueError("Test case failed for Part B")

    answer_a, answer_b = solve(puzzle.input_data)
    puzzle.answer_a = answer_a
    if answer_b != "None":
        puzzle.answer_b = answer_b
