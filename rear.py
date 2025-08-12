import os
from time import sleep
from copy import copy
from utils import get_dataset, parse_fasta
import sys
import tty
import termios
from enum import Enum


class Key(Enum):
    RIGHT = "right"
    LEFT = "left"
    UP = "up"
    DOWN = "down"
    ENTER = "enter"
    BACKSPACE = "backspace"
    EXIT = "exit"


def get_key() -> Key | str:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)

        if ch == "\x1b":  # ESC sequence
            ch += sys.stdin.read(2)
            match ch:
                case "\x1b[C":
                    return Key.RIGHT
                case "\x1b[D":
                    return Key.LEFT
                case "\x1b[A":
                    return Key.UP
                case "\x1b[B":
                    return Key.DOWN
                case _:
                    return ch

        if ch == "\x03":  # Ctrl+c
            return Key.EXIT
        elif ch == "\r" or ch == "\n":
            return Key.ENTER
        elif ch == "\x7f":
            return Key.BACKSPACE

        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


sample = """
1 2 3 4 5 6 7 8 9 10
3 1 5 2 7 4 9 6 10 8

3 10 8 2 5 4 7 1 6 9
5 2 3 1 7 4 10 8 6 9

8 6 7 9 4 1 3 10 2 5
8 2 7 6 9 1 5 3 10 4

3 9 10 4 1 8 6 7 5 2
2 9 8 5 1 7 3 4 6 10

1 2 3 4 5 6 7 8 9 10
1 2 3 4 5 6 7 8 9 10
""".strip()


def parse_dataset(inp):
    lines = iter(inp.split("\n"))

    def parse_line(line):
        return list(map(int, line.split()))

    res = []
    while True:
        res.append((parse_line(next(lines)), parse_line(next(lines))))
        try:
            next(lines)
        except StopIteration:
            break
    return res


black = lambda s: f"\033[0;30m{s}\033[0m"
red = lambda s: f"\033[0;31m{s}\033[0m"
green = lambda s: f"\033[0;32m{s}\033[0m"
yellow = lambda s: f"\033[0;33m{s}\033[0m"
blue = lambda s: f"\033[0;34m{s}\033[0m"
magenta = lambda s: f"\033[0;35m{s}\033[0m"
cyan = lambda s: f"\033[0;36m{s}\033[0m"
white = lambda s: f"\033[0;37m{s}\033[0m"
grey = lambda s: f"\033[2;37m{s}\033[0m"

cell_width = 2


def display(diff):
    for n in diff:
        s = format(abs(n), ">" + str(cell_width))
        if n < 0:
            s = red(s)
        elif n > 0:
            s = blue(s)
        else:
            s = green(s)
        print(s, end="")
    dist = sum(map(abs, diff))
    print("   " + grey(str(dist)))


def flip(diff, start, end):
    diff = copy(diff)
    while (d := end - start) > 0:
        diff[start], diff[end] = diff[end] + d, diff[start] - d
        start += 1
        end -= 1
    return diff


def clear():
    os.system("clear")


class Cursor:
    def __init__(self, length):
        self.reset()
        self.length = length

    def reset(self):
        self._left = 0
        self._right = None

    @staticmethod
    def display_cursors(left, right):
        res = cell_width * " " * (left) + format("^", ">" + str(cell_width))
        if right:
            res += cell_width * " " * (right - left - 1) + format(
                "^", ">" + str(cell_width)
            )
        return res

    def display(self):
        return self.display_cursors(self._left, self._right)

    def move_right(self):
        if self._right is None:
            self._left = min(self.length - 2, self._left + 1)
        else:
            self._right = min(self.length - 1, self._right + 1)

    def move_left(self):
        if self._right is None:
            self._left = max(0, self._left - 1)
        else:
            self._right = max(self._left + 1, self._right - 1)

    def submit(self):
        if self._right is None:
            self._right = self._left + 1
            return
        t = (self._left, self._right, None)
        self.reset()
        return t

    def undo(self):
        if self._right is None:
            self.reset()
            return True
        self._right = None
        return False


def interactive(a, b, goal=None):
    pos = {}
    for i, n in enumerate(a):
        pos[n] = i

    bdiff = []
    for i, n in enumerate(b):
        bdiff.append(pos[n] - i)

    cursor = Cursor(length=len(a))
    sys.stdout.write("\033[?25l")  # hide cursor
    sys.stdout.flush()

    flips = []
    while True:
        clear()

        print("  " + yellow("Backspace") + grey(" undo | "), end="")
        print(yellow("h") + grey("/") + yellow("l") + grey(" left/right | "), end="")
        print(yellow("Enter") + grey(" submit"), end="")
        print()
        if goal:
            print("  Goal:", goal)
        print()

        diff = bdiff
        display(diff)
        for i, (left, right, _) in enumerate(flips):
            print(
                format(
                    cursor.display_cursors(left, right), "<" + str(cell_width * len(a))
                ),
                end=" ",
            )
            print(f"({i + 1})")
            diff = flip(diff, left, right)
            display(diff)

        print(cursor.display())

        key = get_key()
        if key == Key.EXIT:
            break
        if key == Key.RIGHT or key == "l":
            cursor.move_right()
        elif key == Key.LEFT or key == "h":
            cursor.move_left()
        elif key == Key.ENTER:
            if new_flip := cursor.submit():
                flips.append(new_flip)

        elif key == Key.BACKSPACE:
            if cursor.undo() and len(flips) > 0:
                flips.pop()

        else:
            print("unknown key:", key)
            sleep(0.5)

    # show cursor
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


def flip_v2(diff, inv_diff, start, end):
    """
    diff: [..., x, ...]
            x at position i
            element at position i must be shifted to the right by x
            if x is negative, to the left

    inv_diff: [ ..., x, ... ]
              x is at position i
              element at position i + x should be at position i
    """
    diff = copy(diff)
    inv_diff = copy(inv_diff)
    left, right = start, end
    while (d := right - left) > 0:
        diff[left], diff[right] = diff[right] + d, diff[left] - d
        inv_diff[left + diff[left]] = -diff[left]
        inv_diff[right + diff[right]] = -diff[right]
        left += 1
        right -= 1
    return diff, inv_diff


def optimal_steps(diff, inv_diff) -> list[tuple]:
    # first non-zero on left
    left = 0
    while left < len(diff) and diff[left] == 0:
        left += 1
    if left == len(diff):
        return []

    # first non-zero on right
    right = len(diff) - 1
    while diff[right] == 0:
        right -= 1

    left_swap = (left, left + inv_diff[left])
    right_swap = (right + inv_diff[right], right)

    if left_swap == right_swap:
        diff, inv_diff = flip_v2(diff, inv_diff, *left_swap)
        return [left_swap] + optimal_steps(diff, inv_diff)

    if left_swap[1] < right_swap[0]:
        diff, inv_diff = flip_v2(diff, inv_diff, *left_swap)
        diff, inv_diff = flip_v2(diff, inv_diff, *right_swap)
        return [left_swap, right_swap] + optimal_steps(diff, inv_diff)

    lopt = optimal_steps(*flip_v2(diff, inv_diff, *left_swap))
    ropt = optimal_steps(*flip_v2(diff, inv_diff, *right_swap))

    if len(lopt) <= len(ropt):
        res = [left_swap] + lopt
    else:
        res = [right_swap] + ropt

    return res


def main(a, b, verbose=0):
    if verbose > 0:
        print(a)
        print(b)
    posa = {}
    for i, n in enumerate(a):
        posa[n] = i

    posb = {}
    for i, n in enumerate(b):
        posb[n] = i

    bdiff = []
    for i, n in enumerate(b):
        bdiff.append(posa[n] - i)

    # [9, 0, ...]
    # 9 at position 0 means that the number that should be
    # in its place (at position 0) is 9 steps after 0, i.e. 0 + 9 = index 9
    inv_diff = []
    for i, n in enumerate(a):
        inv_diff.append(posb[n] - i)

    def fmt(s):
        return format(s, "<" + str(cell_width * len(a)))

    swaps = optimal_steps(bdiff, inv_diff)
    diff = bdiff
    if verbose > 0:
        display(diff)
    for i, swap in enumerate(swaps, start=1):
        if verbose > 0:
            print(fmt(Cursor.display_cursors(*swap)), i)
        diff = flip(diff, *swap)
        if verbose > 0:
            display(diff)

    if verbose > 0:
        print("---")

    return len(swaps)


if __name__ == "__main__":
    inp = get_dataset(__file__) or sample
    inp = parse_dataset(inp)

    res = []
    for a, b in inp:
        res.append(str(main(a, b)))
    print(" ".join(res))

    # sample_step_counts = [9, 4, 5, 7, 0]
    # goal = sample_step_counts[i]
    # interactive(a, b, goal)
