from aocd.models import Puzzle
from aocd import submit
import os
from collections import defaultdict, deque
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    data =  [[tuple(map(int,coord.split(","))) for coord in line.split("~")]  for line in puzzle_input.split("\n") ]
    data.sort(key=lambda block: block[0][2])
    return [
        {
            (x, y, z)
            for x in range(x1, x2 + 1)
            for y in range(y1, y2 + 1)
            for z in range(z1, z2 + 1)
        }
        for (x1, y1, z1), (x2, y2, z2) in data
    ]

def on_ground(block):
    return any(coord[-1] == 0 for coord in block)



def go_lower(d):
    (x1,y1,z1),(x2,y2,z2) = d    
    return [(x1,y1,z1-1),(x2,y2,z2-1) ] 
 
def do_gravity (blocks):
    occupied = {}
    supports = {i: set() for i in range(len(blocks))}
    for i, block in enumerate(blocks):
        next_coord = {(x, y, z - 1) for x, y, z in block}
        intersected = {occupied[coord] for coord in next_coord if coord in occupied}
        while not intersected and not on_ground(next_coord):
            block = next_coord
            next_coord = {(x, y, z - 1) for x, y, z in block}
            intersected = {occupied[coord] for coord in next_coord if coord in occupied}
        occupied |= {coord: i for coord in block}
        for parent in intersected:
            supports[parent].add(i)
    return supports

def supported_blocks(supports):
    supported = defaultdict(set)
    for parent, children in supports.items():
        for child in children:
            supported[child].add(parent)
    return supported

def do_gravity_check (data, block):
    for d in data:
        if d == block:
            continue
        if not on_ground(d) and not any(intersect(d, s) for s in data if s != block):
            return True
    return False

def part1(data):
    """Solve part 1."""
    supports = do_gravity(data)
    supported = supported_blocks(supports)
    safe = {
        parent
        for parent, children in supports.items()
        if not children or all(len(supported[child]) > 1 for child in children)
    }
    return (len(safe))

def bfs(graph, supported, root):
    count = 0
    removed = set()
    queue = deque([root])
    while queue:
        current = queue.popleft()
        removed.add(current)
        for child in graph[current]:
            if not supported[child] - removed:
                count += 1
                queue.append(child)
    return count

def part2(data):
    """Solve part 2."""
    supports = do_gravity(data)
    supported = supported_blocks(supports)
    safe = {
        parent
        for parent, children in supports.items()
        if not children or all(len(supported[child]) > 1 for child in children)
    }
    unsafe = set(range(len(data))) - safe
    return sum(bfs(supports, supported, block) for block in unsafe)


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
