from math import factorial
from utils import get_dataset, parse_dataset

sample = """
>Rosalind_23
AGCUAGUCAU
""".strip()

if __name__ == "__main__":
    s = parse_dataset(get_dataset(__file__) or sample)[0]
    print(factorial(s.count("A")) * factorial(s.count("G")))
