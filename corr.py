import sys
from revp import complement_dna
from splc import get_dataset, parse_dataset


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


def diff(a, b):
    res = 0
    for aa, bb in zip(a, b):
        if aa != bb:
            res += 1
    return res


def reverse_complement(r):
    return complement_dna(r)[::-1]


if __name__ == "__main__":
    if "--dataset" in sys.argv:
        inp = get_dataset(__file__)
    else:
        inp = sample
    inp = parse_dataset(inp)
    seen = {}
    corrections = {}
    for r in inp:
        rev_comp = reverse_complement(r)

        r1 = seen.get(r[::2])
        r2 = seen.get(r[1::2])
        rv1 = seen.get(rev_comp[::2])
        rv2 = seen.get(rev_comp[1::2])

        if r1 and r2 and r1 == r2:
            # assert r1 == r2, f"{r1} and {r2}"
            continue

        if rv1 and rv2:
            assert rv1 == rv2
            continue

        def make_correction(err, correction):
            if err in corrections:
                # assert err != corrections[err]
                # if correction != corrections[err]:
                #     print(f"{'err:':<20} {err}")
                #     # print(f"{'correction:':<20} {correction}")
                #     print(f"{'corrections[err]:':<20} {corrections[err]}")
                #     print(diff(err, corrections[err]))
                #     raise Exception()
                # assert (
                #     correction == corrections[err]
                # ), f"{err} {correction}, {corrections[err]}"
                del corrections[err]
                err, correction = correction, err
            corrections[err] = correction

        if r1 and diff(r1, r) == 1:
            make_correction(r, r1)
        elif r2 and diff(r2, r) == 1:
            make_correction(r, r2)
        elif rv1 and diff(rv1, rev_comp) == 1:
            make_correction(rev_comp, rv1)
        elif rv2 and diff(rv2, rev_comp) == 1:
            make_correction(rev_comp, rv2)
        else:
            seen[r[::2]] = r
            seen[r[1::2]] = r

    for r in inp:
        correct = None
        if r in corrections:
            correct = corrections[r]
        else:
            rev_comp = reverse_complement(r)
            if rev_comp in corrections:
                correct = reverse_complement(corrections[rev_comp])
        if correct:
            print(f"{r}->{correct}")
            assert diff(r, correct) == 1
