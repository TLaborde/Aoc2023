from aocd.models import Puzzle
from aocd import submit
import os
from collections import defaultdict
import re
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split("\n")]


def do_rec_magic(springs, conditions):
    arrangements = []
    arrangements.append(springs)
    while conditions:
        condition = conditions.pop(0)
        new_ar = []
        for ar in arrangements:
            # s = r"(?=([\?#]{" + re.escape(condition) + r"}))"
            s = r"(?=([\?#]{" + re.escape(condition) + r"}))"
            for match in re.finditer(s, ar):
                if len(ar) >= match.end(1) and "#" not in ar[0:max(0, match.start(1))] and (len(ar) == match.end(1) or ar[match.end(1)] != "#"):
                    new_ar.append(ar[match.end(1) + 1::])
        arrangements = new_ar
    arrangements = [ar for ar in arrangements if "#" not in ar]
    return len(arrangements)


def do_rec_magic2(springs, conditions):
    arrangements = defaultdict(lambda: 0)
    arrangements[springs] += 1
    while conditions:
        condition = conditions.pop(0)
        new_ar = defaultdict(lambda: 0)
        for ar in arrangements.keys():
            # s = r"(?=([\?#]{" + re.escape(condition) + r"}))"
            s = r"(?=([\?#]{" + re.escape(condition) + r"}))"
            for match in re.finditer(s, ar):
                if len(ar) >= match.end(1) and "#" not in ar[0:max(0, match.start(1))] and (len(ar) == match.end(1) or ar[match.end(1)] != "#"):
                    new_ar[ar[match.end(1) + 1::]] += arrangements[ar]
        arrangements = new_ar
    arrangements = sum([v for k, v in arrangements.items() if "#" not in k])
    return arrangements


def part1(data):
    """Solve part 1."""
    result = 0
    for line in data:
        springs, conditions = line.split()
        # springs = [char for char in springs]
        conditions = conditions.split(",")
        result += do_rec_magic2(springs, conditions)
    return result


def part2(data):
    """Solve part 2."""
    result = 0
    for line in data:
        springs, conditions = line.split()
        springs = springs + "?" + springs + "?" + \
            springs + "?" + springs + "?" + springs
        conditions = conditions + "," + conditions + "," + \
            conditions + "," + conditions + "," + conditions
        # springs = [char for char in springs]
        # conditions = [int(i) for i in conditions.split(",")]
        # springs = [len(s) for s in springs.split(".")]
        conditions = conditions.split(",")
        result += do_rec_magic2(springs, conditions)
        print(result)
    return result


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return f"{solution1}", f"{solution2}"


if __name__ == "__main__":
    for example in puzzle.examples:
        data = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
        result_a, result_b = solve(data)
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
