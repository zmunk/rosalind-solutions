from collections import deque
from utils import get_dataset


sample = """
ATCTGAT
TGCATA
""".strip()


def print_grid(grid):
    def wrapper(*args, **kwargs):
        for line in grid(*args, **kwargs):
            print(line)

    return wrapper


@print_grid
def grid(string0, string1, intersections, counts, path):
    width, height = (len(string0), len(string1))
    max_width = None
    cell_width = 3

    top_axis = "  " + " " * cell_width
    for c in string0:
        if max_width and len(top_axis) + cell_width > max_width:
            break
        top_axis += format(c, f">{cell_width}")
    yield top_axis

    for j in range(-1, height):
        if j < 0:
            line = "  "
        else:
            line = string1[j] + " "
        line_width = len(line)

        for i in range(-1, width):
            filters = []
            if (i, j) in counts:
                n = counts[(i, j)]
                if n >= 100:
                    filters.append("cyan")
                c = str(n)[:2]
            elif i < 0 or j < 0:
                c = " "
            elif (i, j) in intersections:
                c = "x"
            else:
                c = "."

            if (i, j) in intersections:
                filters.append("bold")

            if (i, j) in path:
                filters.append("invert")

            num_len = len(str(c))
            c = apply_filters(c, filters)
            c = " " * (cell_width - num_len) + c

            if max_width and line_width + cell_width > max_width:
                break
            line_width += cell_width
            line += c
        yield line


def get_intersections(string0, string1):
    intersections = set()
    for i, c0 in enumerate(string0):
        for j, c1 in enumerate(string1):
            if c0 == c1:
                intersections.add((i, j))

    return intersections


def show_subsequences(string0, string1, supersequence):
    for s in [string0, string1]:
        it = iter(s)
        cc = next(it)
        d = ""
        for c in supersequence:
            if c == cc:
                d += c
                cc = next(it)
            else:
                d += "."
        print(d)


def shortest_common_supersequence(string0, string1, show_grid=False):
    string0 += "x"
    string1 += "x"

    def is_intersection(i, j):
        if i < 0 or j < 0:
            return False
        if i >= len(string0) or j >= len(string1):
            return False
        return string0[i] == string1[j]

    counts = {}
    parents = {}

    q = deque()
    q.append(((-1, -1), 0, None))

    while q:
        loc, count, parent = q.popleft()

        i, j = loc

        if i >= len(string0) or j >= len(string1):
            continue

        if loc in counts and count >= counts[loc]:
            continue

        counts[loc] = count
        parents[loc] = parent

        if is_intersection(i, j):
            next_loc = (i + 1, j + 1)
            if is_intersection(*next_loc):
                q.append((next_loc, count + 1, loc))
            else:
                q.append((next_loc, count + 2, loc))
        else:
            for next_loc in [(i, j + 1), (i + 1, j)]:
                if is_intersection(*next_loc):
                    q.append((next_loc, count, loc))
                else:
                    q.append((next_loc, count + 1, loc))

    intersections = get_intersections(string0, string1)

    end = (len(string0) - 1, len(string1) - 1)

    curr = end
    path = set()
    res = ""
    while True:
        path.add(curr)
        next_node = parents[curr]
        if next_node is None:
            break
        i, j = next_node

        if next_node[0] == curr[0]:
            if j >= 0:
                res += string1[j]
        else:
            if i >= 0:
                res += string0[i]
        curr = next_node

    if show_grid:
        grid(string0, string1, intersections, counts, path)

    return res.strip("x")[::-1]


# curl cheat.sh/ansi
dim = lambda s: f"\033[2;97m{s}\033[0m"
bold = lambda s: f"\033[1;97m{s}\033[0m"
# yellow_dim = lambda s: f"\033[2;33m{s}\033[0m"
# yellow_bold = lambda s: f"\033[1;33m{s}\033[0m"
# cyan_dim = lambda s: f"\033[2;36m{s}\033[0m"
# cyan_bold = lambda s: f"\033[1;36m{s}\033[0m"


def apply_filters(text, filters):
    if "cyan" in filters:
        if "bold" in filters:
            if "invert" in filters:
                # inverted bold cyan
                return f"\033[0;30;106m{text}\033[0m"
            else:
                # bold cyan
                return f"\033[0;36m{text}\033[0m"

        else:
            if "invert" in filters:
                # inverted cyan
                return f"\033[0;30;44m{text}\033[0m"
            else:
                # cyan
                return f"\033[2;34m{text}\033[0m"

    if "bold" in filters:
        if "invert" in filters:
            # bold inverted
            return f"\033[0;30;107m{text}\033[0m"
        else:
            # bold
            return bold(text)  # [1;97m

    if "invert" in filters:
        # inverted
        return f"\033[100;30m{text}\033[0m"

    return dim(text)  # [2;97m


if __name__ == "__main__":
    inp = get_dataset(__file__) or sample
    string0, string1 = inp.split("\n")
    print(shortest_common_supersequence(string0, string1, show_grid=False))
