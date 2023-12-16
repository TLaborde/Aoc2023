from aocd.models import Puzzle
import os

# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [list(line) for line in puzzle_input.split()]

def  try_move_beam(beam, max_length,max_height):
    if beam[2] == "r":
        beam[1] += 1
    if beam[2] == "l":
        beam[1] -= 1
    if beam[2] == "u":
        beam[0] -= 1
    if beam[2] == "d":
        beam[0] += 1
    if 0 <=beam[0] <max_height and 0 <= beam[1] < max_length:
        return beam
    return None
    
def part1(data ,starter = [0,-1,'r']):
    """Solve part 1."""
    max_length = len(data[0])
    max_height = len(data)
    beams = [starter]
    energized = []
    calculated = []
    while beams:
        new_beams = []
        for beam in beams:
            if beam in calculated:
                continue
            else:
                calculated.append(beam.copy())
            if [beam[0],beam[1]] not in energized:
                energized.append([beam[0],beam[1]])
            beam = try_move_beam(beam, max_length,max_height)
            if beam:
                tile = data[beam[0]][beam[1]]
                if tile == ".":
                    new_beams.append(beam)
                if tile == "-" and beam[2] in ["r","l"]:
                    new_beams.append(beam)
                    continue
                if tile == "|" and beam[2] in ["u","d"]:
                    new_beams.append(beam)
                    continue
                if tile == "-":
                    new_beams.append([beam[0],beam[1],"l"])
                    new_beams.append([beam[0],beam[1],"r"])
                if tile == "|":
                    new_beams.append([beam[0],beam[1],"u"])
                    new_beams.append([beam[0],beam[1],"d"])
                if tile == "/":
                    if beam[2] == "r":
                        new_beams.append([beam[0],beam[1],"u"])
                    if beam[2] == "u":
                        new_beams.append([beam[0],beam[1],"r"])
                    if beam[2] == "l":
                        new_beams.append([beam[0],beam[1],"d"])
                    if beam[2] == "d":
                        new_beams.append([beam[0],beam[1],"l"])
                if tile == "\\":
                    if beam[2] == "r":
                        new_beams.append([beam[0],beam[1],"d"])
                    if beam[2] == "u":
                        new_beams.append([beam[0],beam[1],"l"])
                    if beam[2] == "l":
                        new_beams.append([beam[0],beam[1],"u"])
                    if beam[2] == "d":
                        new_beams.append([beam[0],beam[1],"r"])
        beams = new_beams
    print (starter, len(energized) -1)
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
