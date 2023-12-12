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


def compute(springs, conditions):
    arrangements = defaultdict(lambda: 0)
    arrangements[springs] += 1
    for condition in conditions:
        new_ar = defaultdict(lambda: 0)
        for ar in arrangements:
            s = rf'(?=([\?#]{{{re.escape(condition)}}})([^#]+|$))'
            for match in re.finditer(s, ar):
                if len(ar) >= match.end(1) and "#" not in ar[0:max(0, match.start(1))]:
                    new_ar[ar[match.end(1) + 1::]] += arrangements[ar]
        arrangements = new_ar

    return sum(v for k, v in arrangements.items() if "#" not in k)


def part1(data):
    """Solve part 1."""
    result = 0
    for line in data:
        springs, conditions = line.split()
        conditions = conditions.split(",")
        result += compute(springs, conditions)
    return result


def part2(data):
    """Solve part 2."""
    result = 0
    for line in data:
        springs, conditions = line.split()
        springs = '?'.join([springs] * 5)
        conditions = [condition for _ in range(
            5) for condition in conditions.split(',')]
        result += compute(springs, conditions)
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
