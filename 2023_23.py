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
    source = [line for line in puzzle_input.split()]
    G = defaultdict(list)
    for i, line in enumerate(source):
        for j,c in enumerate(line):
            if c == '.':
                if i-1 >= 0 and source[i-1][j] != '#':
                    G[(i,j)].append((i-1,j))
                if j-1 >= 0 and source[i][j-1] != '#':
                    G[(i,j)].append((i,j-1))
                if i+1 <len(source) and source[i+1][j] != '#':
                    G[(i,j)].append((i+1,j))
                if j+1 <len(line) and source[i][j+1] != '#':
                    G[(i,j)].append((i,j+1))
            elif c != '#':
                if c == '>' and source[i][j+1] != '#':
                    G[(i,j)].append((i,j+1))
                if c == '<' and source[i][j-1] != '#':
                    G[(i,j)].append((i,j-1))
                if c == '^' and source[i-1][j] != '#':
                    G[(i,j)].append((i-1,j))
                if c == 'v' and source[i+1][j] != '#':
                    G[(i,j)].append((i+1,j))
    entrance = (0,1)
    exit_point = (len(source)-1,len(source[0])-2)
    return G, entrance, exit_point

def parse2(puzzle_input):
    """Parse input."""
    source = [line for line in puzzle_input.split()]
    entrance = (0,1)
    exit_point = (len(source)-1,len(source[0])-2)
    G = defaultdict(list)
    for i, line in enumerate(source):
        for j,c in enumerate(line):
            if c != '#':
                if i-1 >= 0 and source[i-1][j] != '#':
                    G[(i,j)].append((i-1,j))
                if j-1 >= 0 and source[i][j-1] != '#':
                    G[(i,j)].append((i,j-1))
                if i+1 <len(source) and source[i+1][j] != '#':
                    G[(i,j)].append((i+1,j))
                if j+1 <len(line) and source[i][j+1] != '#':
                    G[(i,j)].append((i,j+1))
    crossings = [k for k,v in G.items() if len(v)>2]
    compressed_G = defaultdict(set)
    for p1 in crossings:
        for p2 in crossings:
            if p1 != p2:
                path = bfs(G,p1,p2,crossings)
                dist = len(path)
                if dist:
                    compressed_G[p1].add((p2,dist))
                    compressed_G[p2].add((p1,dist))
        p2 = entrance
        path = bfs(G,p1,p2,crossings)
        dist = len(path)
        if dist:
            compressed_G[p2].add((p1,dist))
        p2 = exit_point
        path = bfs(G,p1,p2,crossings)
        dist = len(path)
        if dist:
            compressed_G[p1].add((p2,dist))

    return compressed_G, entrance, exit_point

def bfs(G, entrance, exit_point, crossings):
    # current, visited
    branches = deque()
    branches.append((entrance, set()))
    longest_path= set()
    while branches:
        current, visited = branches.pop()
        if current == exit_point and len(visited) > len(longest_path):
            longest_path=visited
        else:
            for n in G[current]:
                visited.add(current)
                if n not in visited and (n not in crossings or n == exit_point):
                    branches.append((n,set(visited)))
    return longest_path

def part1(data):
    """Solve part 1."""
    G, entrance, exit_point = data
    # current, visited
    branches = deque()
    branches.append((entrance, set()))
    max_length = 0
    while branches:
        current, visited = branches.pop()
        if current == exit_point and len(visited) > max_length:
            max_length = len(visited)
        else:
            for n in G[current]:
                visited.add(current)
                if n not in visited:
                    branches.append((n,set(visited)))
    return max_length


def part2(data):
    G, entrance, exit_point = data
    # current, visited, distance
    branches = deque()
    branches.append((entrance, set(), 0))
    max_length = 0
    while branches:
        if len(branches) % 10 == 0:
            print(len(branches))
        current, visited, distance = branches.pop()
        if current == exit_point and distance > max_length:
            max_length = distance
        else:
            visited.add(current)
            for (n,extra_dist) in G[current]:
                if n not in visited:
                    branches.append((n,set(visited), distance+extra_dist))
    return max_length
    return None


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse2(puzzle_input)
    solution2 = part2(data)

    return f"{solution1}", f"{solution2}"


if __name__ == "__main__":
    for example in puzzle.examples:
        result_a, result_b = solve(example.input_data)
        if result_a != '94':
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
