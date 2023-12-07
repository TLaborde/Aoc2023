from aocd.models import Puzzle
from aocd import submit
import os
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    data = [line for line in puzzle_input.split("\n")]
    return [x.split() for x in data]


def hand_sort(hands):
    types = [('five_kind', []), ('four_kind', []), ('full', []),
             ('three_kind', []), ('two_pair', []), ('one_pair', []), ('high', [])]
    for hand in hands:
        cards = hand[0]
        chars = {char: cards.count(char) for char in set(cards)}
        counts = list(chars.values())
        if 5 in counts:
            types[0][1].append(hand)
            continue
        if 4 in counts:
            types[1][1].append(hand)
            continue
        if 3 in counts and 2 in counts:
            types[2][1].append(hand)
            continue
        if 3 in counts:
            types[3][1].append(hand)
            continue
        if 2 in [counts.count(n) for n in counts]:
            types[4][1].append(hand)
            continue
        if 2 in counts:
            types[5][1].append(hand)
            continue
        types[6][1].append(hand)

    alphabet = {c: i for i, c in enumerate("AKQJT98765432")}
    return list(reversed(list(hand for _, hands in types for hand in sorted(hands, key=lambda word: tuple(alphabet.get(c, ord(c)) for c in word[0])))))


def hand_sort2(hands):
    types = [('five_kind', []), ('four_kind', []), ('full', []),
             ('three_kind', []), ('two_pair', []), ('one_pair', []), ('high', [])]
    for hand in hands:
        cards = hand[0]
        chars = {char: cards.count(char) for char in set(cards)}
        joker = chars.pop('J', 0)
        counts = [0] if not chars.values() else list(chars.values())
        max_rep = max(counts) if counts else 0
        if max_rep+joker == 5:
            types[0][1].append(hand)
            continue
        if max_rep+joker == 4:
            types[1][1].append(hand)
            continue
        if 3 in counts and 2 in counts or ([2, 2] == counts and joker == 1):
            types[2][1].append(hand)
            continue
        if 3 in counts or (2 in counts and joker == 1) or (joker == 2):
            types[3][1].append(hand)
            continue
        if 2 in [counts.count(n) for n in counts]:
            types[4][1].append(hand)
            continue
        if 2 in counts or joker == 1:
            types[5][1].append(hand)
            continue
        types[6][1].append(hand)

    alphabet = {c: i for i, c in enumerate("AKQJT98765432J")}

    return list(reversed(list(hand for _, hands in types for hand in sorted(hands, key=lambda word: tuple(alphabet.get(c, ord(c)) for c in word[0])))))


def part1(data):
    """Solve part 1."""
    sorted_hands = hand_sort(data)
    result_sum = sum((i+1) * int(hand[1])
                     for i, hand in enumerate(sorted_hands))
    return result_sum


def part2(data):
    """Solve part 2."""
    sorted_hands = hand_sort2(data)
    result_sum = sum((i+1) * int(hand[1])
                     for i, hand in enumerate(sorted_hands))
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
