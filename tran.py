import sys
from utils import get_dataset, parse_dataset

sample = """
>Rosalind_0209
GCAACGCACAACGAAAACCCTTAGGGACTGGATTATTTCGTGATCGTTGTAGTTATTGGA
AGTACGGGCATCAACCCAGTT
>Rosalind_2200
TTATCTGACAAAGAAAGCCGTCAACGGCTGGATAATTTCGCGATCGTGCTGGTTACTGGC
GGTACGAGTGTTCCTTTGGGT
""".strip()

if __name__ == "__main__":
    inp = parse_dataset(get_dataset(__file__) or sample)

    s1, s2 = inp

    ts, tv = 0, 0
    for a, b in zip(s1, s2):
        if a == b:
            continue
        match a + b:
            case "AG" | "GA" | "CT" | "TC":
                ts += 1
            case _:
                tv += 1
    print(ts / tv)
