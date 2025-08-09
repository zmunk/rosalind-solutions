from splc import parse_dataset


sample = """
>Rosalind_6431
CTTCGAAAGTTTGGGCCGAGTCTTACAGTCGGTCTTGAAGCAAAGTAACGAACTCCACGG
CCCTGACTACCGAACCAGTTGTGAGTACTCAACTGGGTGAGAGTGCAGTCCCTATTGAGT
TTCCGAGACTCACCGGGATTTTCGATCCAGCCTCAGTCCAGTCTTGTGGCCAACTCACCA
AATGACGTTGGAATATCCCTGTCTAGCTCACGCAGTACTTAGTAAGAGGTCGCTGCAGCG
GGGCAAGGAGATCGGAAAATGTGCTCTATATGCGACTAAAGCTCCTAACTTACACGTAGA
CTTGCCCGTGTTAAAAACTCGGCTCACATGCTGTCTGCGGCTGGCTGTATACAGTATCTA
CCTAATACCCTTCAGTTCGCCGCACAAAAGCTGGGAGTTACCGCGGAAATCACAG
""".strip()


def find_and_move(s, sub) -> str | None:
    """
    Return s[i+1:] where i is the first occurrence of sub in s
    if one is found, otherwaise return None.
    """
    try:
        i = s.index(sub)
    except ValueError:
        return None
    return s[i + 1 :]


def count_occurrences(s, sub):
    res = 0
    while s := find_and_move(s, sub):
        res += 1
    return res


def quat_to_dec(s):
    """
    convert quaternary to decimal, where A = 0, C = 1, G = 2, T = 3
    e.g. AAAA -> 0
         AAAT -> 3
         CAAA -> 64
    """
    if s == "":
        return 0
    res = 4 * quat_to_dec(s[:-1])
    match s[-1]:
        case "A":
            res += 0
        case "C":
            res += 1
        case "G":
            res += 2
        case "T":
            res += 3
        case _:
            raise ValueError(f"unknown char: {s[-1]}")
    return res


if __name__ == "__main__":
    inp = parse_dataset(get_dataset(__file__) or sample)[0]

    comp = [0] * 256

    for start in range(len(inp) - 3):
        comp[quat_to_dec(inp[start : start + 4])] += 1
    print(" ".join(map(str, comp)))
