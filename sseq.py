import sys
from splc import get_dataset, parse_dataset

sample = """
>Rosalind_14
ACGTACGTGACG
>Rosalind_18
GTA
""".strip()

if __name__ == "__main__":
    if "--dataset" in sys.argv:
        inp = get_dataset(__file__)
    else:
        inp = sample

    inp = parse_dataset(inp)
    s, sub = inp

    # print(s)
    # print(sub)

    si = 0
    indices = []
    for i, c in enumerate(s):
        if c != sub[si]:
            continue
        indices.append(i)
        si += 1
        if si >= len(sub):
            break

    res = []
    for i in indices:
        res.append(str(i + 1))

    print(" ".join(res))
