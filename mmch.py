from collections import Counter
from utils import get_dataset, parse_fasta


sample = """
>Rosalind_92
AUGCUUC
""".strip()

if __name__ == "__main__":
    inp = parse_fasta(get_dataset(__file__) or sample)[0]
    c = Counter(inp)
    res = 1
    for a, b in [("A", "U"), ("G", "C")]:
        for i in range(max(c[a], c[b]), abs(c[a] - c[b]), -1):
            res *= i
    print(res)
