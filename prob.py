import sys
from splc import get_dataset, parse_dataset
from math import log10


def get_prob(s, gcc):
    log_at = log10((1 - gcc) / 2)
    log_gc = log10(gcc / 2)

    acc = 0
    for c in s:
        if c in "AT":
            acc += log_at
        else:
            acc += log_gc
    return format(acc, ".3f")


sample = """
ACGATACAA
0.129 0.287 0.423 0.476 0.641 0.742 0.783
""".strip()

if __name__ == "__main__":
    if "--dataset" in sys.argv:
        inp = get_dataset(__file__)
    else:
        inp = sample

    s, a = inp.split("\n")
    gccs = list(map(float, a.split()))
    res = ""
    print(" ".join([get_prob(s, gcc) for gcc in gccs]))
