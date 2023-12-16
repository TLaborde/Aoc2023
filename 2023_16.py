from aocd.models import Puzzle
import os

from enum import Enum

class Direction(Enum):
    RIGHT = "r"
    LEFT = "l"
    UP = "u"
    DOWN = "d"

# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [list(line) for line in puzzle_input.split()]

def try_move_beam(beam, max_length, max_height):
    x, y, direction = beam
    if direction == 'r':
        y += 1
    elif direction == 'l':
        y -= 1
    elif direction == 'u':
        x -= 1
    elif direction == 'd':
        x += 1

    if 0 <= x < max_height and 0 <= y < max_length:
        return [x, y, direction]
    return None

    
def part1(data ,starter = [0,-1,'r']):
    """Solve part 1."""
    max_length = len(data[0])
    max_height = len(data)
    beams = [starter]
    energized = []
    calculated = []
    tile_directions = {
        "-": ["l", "r"],
        "|": ["u", "d"],
        "/": {"r": "u", "u": "r", "l": "d", "d": "l"},
        "\\": {"r": "d", "u": "l", "l": "u", "d": "r"}
    }
    while beams:
        new_beams = []
        for beam in beams:
            if beam in calculated:
                continue
            else:
                calculated.append(beam.copy())
            if beam[:2] not in energized:
                energized.append(beam[:2])
            beam = try_move_beam(beam, max_length,max_height)
            if beam:
                tile = data[beam[0]][beam[1]]
                if tile == "." or (beam[2] in tile_directions[tile] and tile in ["-","|"]):
                    new_beams.append(beam)
                else:
                    if isinstance(tile_directions[tile], list):
                        new_beams.extend([beam[0], beam[1], direction] for direction in tile_directions[tile])
                    elif isinstance(tile_directions[tile], dict):
                        new_beams.append([beam[0], beam[1], tile_directions[tile][beam[2]]])
        beams = new_beams
    return (len(energized) -1)


def part2(data):
    """Solve part 2."""

    m1 = max(part1(data,[-1,i,'d']) for i in range(len(data[0])))
    print("m1 done")
    m2 = max(part1(data,[len(data),i,'u'])for i in range(len(data[0])))
    print("m2 done")
    m3 = max(part1(data,[i, -1, 'r'])for i in range(len(data)))
    print("m3 done")
    m4 = max(part1(data,[i,len(data[0]),'l'])for i in range(len(data)))
    return max([m1,m2,m3,m4])


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
            if result_b != '51':
                print(f"Expected {example.answer_b}, got {result_b}")
                raise ValueError("Test case failed for Part B")

    answer_a, answer_b = solve(puzzle.input_data)
    puzzle.answer_a = answer_a
    if answer_b != "None":
        puzzle.answer_b = answer_b
