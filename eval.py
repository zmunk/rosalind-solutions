from utils import get_dataset, parse_fasta


sample = """
10
AG
0.25 0.5 0.75
""".strip()

if __name__ == "__main__":
    inp = get_dataset(__file__) or sample
    inp = inp.split("\n")
    n = int(inp[0])
    s = inp[1]
    a = list(map(float, inp[2].split()))

    m = n - len(s) + 1

    # count of A/T
    # count of G/C
    cnt_at, cnt_gc = 0, 0
    for c in s:
        match c:
            case "A" | "T":
                cnt_at += 1
            case "G" | "C":
                cnt_gc += 1

    res = []
    for gcc in a:
        # probability of getting 'G' or 'C'
        prob_gc = gcc / 2

        # probability of getting 'A' or 'T'
        prob_at = (1 - gcc) / 2

        res.append(format(prob_at**cnt_at * prob_gc**cnt_gc * m, ".3f"))
    print(" ".join(res))
