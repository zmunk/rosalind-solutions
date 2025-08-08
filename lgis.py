import sys
from collections import deque
from bisect import bisect_left
from splc import get_dataset


def get_longest_subsequence(seq, increasing=True, output="list", verbose=0):
    def log(*args, **kwargs):
        if verbose > 0:
            print(*args, **kwargs)

    log(f"{seq = }")
    d = {}
    lengths = {}
    peak = None

    sorted_seq = []
    for n in seq:
        i = bisect_left(sorted_seq, n)

        assert n not in d

        if (increasing and i == 0) or (not increasing and i == len(sorted_seq)):
            d[n] = None
            lengths[n] = 1
        else:
            if increasing:
                prev_ind = i - 1
                assert n > sorted_seq[prev_ind]
            else:
                prev_ind = i
                # prev = sorted_seq[i]
                assert n < sorted_seq[prev_ind]
            # log(f"{prev_ind = }")

            sp = 10

            def fmt(*args):
                for arg in args:
                    log(format(arg, "<" + str(sp)), end="")
                log()

            # log("new:", n)
            fmt("new:", n)
            fmt("sorted:", *map(lambda x: f"{x} [{lengths[x]}]", sorted_seq))
            # fmt("sorted:", *sorted_seq)
            log(" " * (sp * (prev_ind + 1) - 1), "^")
            # fmt("lengths:", *map(lambda x: lengths[x], sorted_seq))
            log()
            # log(format("sorted:", "<" + str(sp)), end="")
            # for m in sorted_seq:
            #     log(format(m, ">" + str(sp)), end="")
            # log()

            # log(format("lengths:", "<" + str(sp)), end="")
            # for m in sorted_seq:
            #     log(format(lengths[m], ">" + str(sp)), end="")
            # log()

            prev = sorted_seq[prev_ind]
            # log(f"prev: {prev}")
            d[n] = prev
            lengths[n] = lengths[prev] + 1
            if peak is None or lengths[n] > lengths[peak]:
                peak = n

                # # log(sorted_seq, i, n)
                # log(f"{n} -> [{i}]")
                # if increasing:
                #     log(d[n], "<", n, f"[{lengths[n]}]")
                # else:
                #     log(d[n], ">", n, f"[{lengths[n]}]")
                # # input()

        sorted_seq.insert(i, n)

        if increasing:
            # for anything to the right of i in sorted_seq,
            # remove any values whose length is <= lengths[n]
            for j in range(len(sorted_seq) - 1, i, -1):
                m = sorted_seq[j]
                if lengths[m] <= lengths[n]:
                    del sorted_seq[j]
        else:
            for j in range(i - 1, -1, -1):
                m = sorted_seq[j]
                if lengths[m] <= lengths[n]:
                    del sorted_seq[j]

    log(f"{sorted_seq = }")
    log(f"d: {d}")

    res = deque()
    curr = peak
    # curr = d[peak]
    while curr:
        res.appendleft(curr)
        # res = str(curr) + " " + res
        curr = d[curr]
    if output == "list":
        return list(res)

    # res = str(peak)
    # curr = d[peak]
    # while curr:
    #     res = str(curr) + " " + res
    #     curr = d[curr]
    return " ".join(map(str, res))


sample = """
5
5 1 4 2 3
""".strip()


def cyan(s):
    return f"\033[0;36m{s}\033[0m"


# cyan_ =    lambda s: f'\033[1;36m{s}\033[0m'

if __name__ == "__main__":
    if "--dataset" in sys.argv:
        inp = get_dataset(__file__)
    else:
        inp = sample
    # print(inp)
    seq = list(map(int, inp.split("\n")[1].split()))
    # seq = [8, 2, 1, 6, 5, 7, 4, 3, 9]
    # print(seq[:10])

    # increasing = get_longest_subsequence(seq, increasing=True, verbose=1)
    increasing = get_longest_subsequence(seq, increasing=True, output="string")
    # decreasing = get_longest_subsequence(seq, increasing=False, verbose=1)
    decreasing = get_longest_subsequence(seq, increasing=False, output="string")

    print(increasing)
    print(decreasing)

    # for i, (a, b) in enumerate(zip(increasing[:-1], increasing[1:])):
    #     assert a < b, f"{increasing[:i]} {a} >= {b}"

    # for a, b in zip(decreasing[:-1], decreasing[1:]):
    #     assert a > b
    # print()
    # print()
    # inc = set(increasing)
    # for n in seq[:100]:
    #     if n in inc:
    #         print(cyan(n), end=" ")
    #     else:
    #         print(n, end=" ")
