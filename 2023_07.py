from aocd.models import Puzzle
from aocd import submit
import os
from collections import defaultdict
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split("\n")]


def hand_sort(hands):
    types = {
        'five_kind': [],
        'four_kind': [],
        'full': [],
        'three_kind': [],
        'two_pair': [],
        'one_pair': [],
        'high': []
    }
    for hand in hands:
        cards = hand[0]
        chars = defaultdict(int)
        for char in cards:
            chars[char] += 1
        counts = list(chars.values())
        if 5 in counts:
            types['five_kind'].append(hand)
            continue
        if 4 in counts:
            types['four_kind'].append(hand)
            continue
        if 3 in counts and 2 in counts:
            types['full'].append(hand)
            continue
        if 3 in counts:
            types['three_kind'].append(hand)
            continue
        if 2 in [counts.count(n) for n in counts]:
            types['two_pair'].append(hand)
            continue
        if 2 in counts:
            types['one_pair'].append(hand)
            continue
        types['high'].append(hand)

    alphabet = {c: i for i, c in enumerate("AKQJT98765432")}
    return_val = []
    for t in ['five_kind', 'four_kind', 'full', 'three_kind', 'two_pair', 'one_pair', 'high']:
        return_val.extend(sorted(types[t], key=lambda word: [
            alphabet.get(c, ord(c)) for c in word[0]]))

    return return_val


def hand_sort2(hands):
    types = {
        'five_kind': [],
        'four_kind': [],
        'full': [],
        'three_kind': [],
        'two_pair': [],
        'one_pair': [],
        'high': []
    }
    for hand in hands:
        cards = hand[0]
        chars = defaultdict(int)
        for char in cards:
            chars[char] += 1
        joker = chars.pop('J', 0)
        counts = [0]
        max_rep = 0
        if chars.values():
            counts = list(chars.values())
            max_rep = max(counts)
        if max_rep+joker == 5:
            types['five_kind'].append(hand)
            continue
        if max_rep+joker == 4:
            types['four_kind'].append(hand)
            continue
        if 3 in counts and 2 in counts or ([2, 2] == counts and joker == 1):
            types['full'].append(hand)
            continue
        if 3 in counts or (2 in counts and joker == 1) or (joker == 2):
            types['three_kind'].append(hand)
            continue
        if 2 in [counts.count(n) for n in counts]:
            types['two_pair'].append(hand)
            continue
        if 2 in counts or joker == 1:
            types['one_pair'].append(hand)
            continue
        types['high'].append(hand)
    for t in ['five_kind', 'four_kind', 'full', 'three_kind', 'two_pair', 'one_pair', 'high']:
        print(t)
        for val in types[t]:
            print(val[0])
    alphabet = {c: i for i, c in enumerate("AKQJT98765432J")}
    return_val = []
    for t in ['five_kind', 'four_kind', 'full', 'three_kind', 'two_pair', 'one_pair', 'high']:
        return_val.extend(sorted(types[t], key=lambda word: [
            alphabet.get(c, ord(c)) for c in word[0]]))

    return return_val


def part1(data):
    """Solve part 1."""
    hands = [x.split(" ") for x in data]
    sorted = hand_sort(hands)
    result_sum = 0
    for i, hand in enumerate(reversed(sorted)):
        result_sum += (i+1) * int(hand[1])
    return result_sum


def part2(data):
    """Solve part 2."""
    hands = [x.split(" ") for x in data]
    sorted = hand_sort2(hands)
    result_sum = 0
    for i, hand in enumerate(reversed(sorted)):
        result_sum += (i+1) * int(hand[1])
    return result_sum


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
