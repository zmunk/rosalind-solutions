from math import factorial
import sys
from splc import get_dataset, parse_dataset

sample = """
>Rosalind_23
AGCUAGUCAU
""".strip()


if "--dataset" in sys.argv:
    inp = get_dataset(__file__)
    s = parse_dataset(inp)[0]
else:
    s = sample.split()[1]
print(factorial(s.count("A")) * factorial(s.count("G")))
# print(inp)
# print(inp.split()[1])
# strings = parse_dataset(inp)
# else:
# strings = sample.split("\n")[1::2]
