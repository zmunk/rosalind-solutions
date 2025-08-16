import os
import time
from collections import defaultdict
from utils import get_dataset, parse_fasta


sample = """
>Rosalind_39
PLEASANTLY
>Rosalind_11
MEANLY
""".strip()

# string0 is the horizontal axis
# string1 is the vertical axis
#   P L E A S A N T L Y
# M
# E     X
# A       X   X
# N             X
# L   X             X
# Y                   X


def get_grid(dimensions, nodes, intersections, seen, fit_term=False):
    width, height = dimensions
    if fit_term:
        size = os.get_terminal_size()
        width = min(width, size.columns)
        height = min(height, size.lines - 4)

    for j in range(height):
        line = ""
        for i in range(width):
            if (i, j) in nodes:
                c = "o"
            elif (i, j) in intersections:
                c = "x"
            elif (i, j) in seen:
                c = "."
            else:
                c = "."
            line += c
        yield line


def show_grid(*args, **kwargs):
    os.system("clear")
    for line in get_grid(*args, **kwargs):
        print(line)


class SearchTermination(Exception):
    pass


def main(string0, string1):
    index0 = defaultdict(list)
    for i, c in enumerate(string0):
        index0[c].append(i)

    len0 = len(string0)
    len1 = len(string1)

    intersections = set()
    for i, c0 in enumerate(string0):
        for j, c1 in enumerate(string1):
            if c0 == c1:
                intersections.add((i, j))

    def get_children(node):
        for child in [
            (node[0] + 1, node[1]),
            (node[0], node[1] + 1),
            (node[0] + 1, node[1] + 1),
        ]:
            if child in intersections:
                while child in intersections:
                    child = (child[0] + 1, child[1] + 1)
            yield child

    seen = set()

    def propagate(prev_nodes):
        for node in prev_nodes:
            for child in get_children(node):
                if child in seen:
                    continue

                if child == (len0, len1):
                    raise SearchTermination

                seen.add(child)
                yield child

    nodes = set(get_children((-1, -1))) - {(-1, 0), (0, -1)}
    seen |= nodes

    step_num = 1
    while len(nodes) > 0:
        ## Debugging
        # show_grid((len0, len1), nodes, intersections, seen, fit_term=True)
        # time.sleep(0.1)
        ############

        try:
            nodes = set(propagate(nodes))
        except SearchTermination:
            return step_num
        step_num += 1

    raise Exception


if __name__ == "__main__":
    inp = parse_fasta(get_dataset(__file__) or sample)
    string0, string1 = inp
    print(main(string0, string1))
