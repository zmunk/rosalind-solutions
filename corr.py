import sys
import hashlib
from collections import defaultdict
from revp import complement_dna
from splc import get_dataset, parse_dataset
from orf import cyan_bold, red_bold


sample = """
>Rosalind_52
TCATC
>Rosalind_44
TTCAT
>Rosalind_68
TCATC
>Rosalind_28
TGAAA
>Rosalind_95
GAGGA
>Rosalind_66
TTTCA
>Rosalind_33
ATCAA
>Rosalind_21
TTGAT
>Rosalind_18
TTTCC
""".strip()


def hash_string(s, length=6):
    return hashlib.sha1(s.encode("UTF-8")).hexdigest()[:length]


def diff(a, b):
    res = 0
    for aa, bb in zip(a, b):
        if aa != bb:
            res += 1
    return res


def reverse_complement(r):
    return complement_dna(r)[::-1]


def get_diff_locations(a, b):
    res = []
    for i, (aa, bb) in enumerate(zip(a, b)):
        if aa != bb:
            res.append(i)
    return res


def green_bold(s):
    return f"\033[1;32m{s}\033[0m"


def highlight_locations(s, locations, default=None):
    res = ""
    for i, c in enumerate(s):
        if i in locations:
            res += red_bold(c)
        elif default:
            res += default(c)
        else:
            res += c
    return res


def show_comparison(s1, s2, labels=None):
    if not labels:
        labels = ["s1", "s2"]
    label_fmt = "<" + str(max(map(len, labels)) + 1)
    locs = set(get_diff_locations(s1, s2))
    print(
        format(labels[0] + ":", label_fmt),
        highlight_locations(s1, locs, default=green_bold),
    )
    print(
        format(labels[1] + ":", label_fmt),
        highlight_locations(s2, locs, default=green_bold),
    )
    print()


def hamming_distance(s1, s2) -> int:
    return len(get_diff_locations(s1, s2))


def main(inp):
    counts = defaultdict(int)  # dna -> number of times it was seen
    lookup = defaultdict(set)  # component -> full dna
    reversed_dnas = set()
    incorrect_dnas = set()
    for raw_dna in inp:
        for rev in [False, True]:
            if rev:
                dna = reverse_complement(raw_dna)
                reversed_dnas.add(dna)
            else:
                dna = raw_dna

            counts[dna] += 1
            if counts[dna] == 1:
                incorrect_dnas.add(dna)
            elif counts[dna] == 2:
                incorrect_dnas.remove(dna)

            # components[0]: every other character starting from 0
            # components[1]: every other character starting from 1
            components = [dna[::2], dna[1::2]]

            for comp in components:
                lookup[comp].add(dna)

    corrections = set()
    for dna in incorrect_dnas - reversed_dnas:
        components = [dna[::2], dna[1::2]]
        similar_dna = None
        for comp in components:
            for sim in lookup[comp]:
                if hamming_distance(dna, sim) == 1 and counts[sim] > 1:
                    similar_dna = sim
                    break
            if similar_dna:
                break
        assert similar_dna is not None
        if dna in reversed_dnas:
            dna = reverse_complement(dna)
            similar_dna = reverse_complement(similar_dna)
        assert hamming_distance(dna, similar_dna) == 1
        assert (dna, similar_dna) not in corrections
        print(dna + "->" + similar_dna)
        corrections.add((dna, similar_dna))


if __name__ == "__main__":
    if "--dataset" in sys.argv:
        inp = get_dataset(__file__)
    else:
        inp = sample
    inp = parse_dataset(inp)
    main(inp)
