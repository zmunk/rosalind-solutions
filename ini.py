from utils import get_dataset
from collections import Counter

sample = "AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC"

if __name__ == "__main__":
    inp = get_dataset(__file__) or sample
    c = Counter(inp)
    print(f"{c['A']} {c['C']} {c['G']} {c['T']} ")
