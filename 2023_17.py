from aocd.models import Puzzle
from aocd import submit
import os
from collections import deque, defaultdict
from queue import PriorityQueue
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [[int(i) for i in line] for line in puzzle_input.split()]


def part1(data, max_dist = 3):
    """Solve part 1."""
    max_height, max_width = len(data), len(data[0])
    grid = {(x, y): int(n) for y, line in enumerate(data) for x, n in enumerate(line)}

    end = (max_height -1 , max_width -1)
    left = (1,0)
    down = (0,1)
    next_nodes = PriorityQueue()
    next_nodes.put((grid[(1, 0)], (1, 0), left, 1))
    next_nodes.put((grid[(0, 1)], (0, 1), down, 1))
    done = set()

    while next_nodes:
        # get will return the next node with the lowest total cost
        cost, (x, y), direction, dist = next_nodes.get()
        if (x,y) == end:
            return cost
        if((x,y),direction,dist) in done:
            continue
        done.add(((x,y),direction,dist))

        #turn right
        right_node = (x -direction[1], y + direction[0])
        if right_node in grid:
            right_cost = cost + grid[right_node]
            next_nodes.put((right_cost,right_node,(-direction[1],direction[0]),0))
        # or turn left
        left_node = (x + direction[1], y - direction[0])
        if left_node in grid:
            left_cost = cost + grid[left_node]
            next_nodes.put((left_cost,left_node,(direction[1],-direction[0]),0))

        # or go straight
        if dist < max_dist -1 and (x + direction[0],y+direction[1]) in grid:
            new_node = (x + direction[0],y+direction[1])
            new_cost = cost + grid[new_node]
            next_nodes.put((new_cost,new_node,direction,dist+1))

def rotate_right(vec):
    return (-vec[1],vec[0])

def rotate_left(vec):
    return (vec[1],-vec[0])

def part2(data, max_dist = 10, min_dist = 3):
    max_height, max_width = len(data), len(data[0])
    grid = {(x, y): int(n) for y, line in enumerate(data) for x, n in enumerate(line)}

    end = (max_height -1 , max_width -1)
    left = (1,0)
    down = (0,1)
    next_nodes = PriorityQueue()
    next_nodes.put((grid[(1, 0)], (1, 0), left, 1))
    next_nodes.put((grid[(0, 1)], (0, 1), down, 1))
    done = set()

    while next_nodes:
        # get will return the next node with the lowest total cost
        cost, (x, y), direction, dist = next_nodes.get()
        if (x,y) == end and min_dist <= dist:
            return cost
        if((x,y),direction,dist) in done:
            continue
        done.add(((x,y),direction,dist))

        # we turn only if we have done enough distance
        if min_dist <= dist:
            #turn right
            rotated_dir = rotate_right (direction)
            new_node = (x + rotated_dir[0] , y + rotated_dir[1])
            if new_node in grid:
                new_cost = cost + grid[new_node]
                next_nodes.put((new_cost,new_node,rotated_dir,0))
            # or turn left
            rotated_dir = rotate_left(direction)
            new_node = (x + rotated_dir[0] , y + rotated_dir[1])
            if new_node in grid:
                new_cost = cost + grid[new_node]
                next_nodes.put((new_cost,new_node,rotated_dir,0))

        # or go straight
        if dist < max_dist -1 and (x + direction[0],y+direction[1]) in grid:
            new_node = (x + direction[0],y+direction[1])
            new_cost = cost + grid[new_node]
            next_nodes.put((new_cost,new_node,direction,dist+1))


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
            if result_b != '94':
                print(f"Expected {example.answer_b}, got {result_b}")
                raise ValueError("Test case failed for Part B")

    answer_a, answer_b = solve(puzzle.input_data)
    puzzle.answer_a = answer_a
    if answer_b != "None":
        puzzle.answer_b = answer_b
