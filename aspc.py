from math import factorial
from utils import get_dataset


sample = """
6 3
""".strip()

if __name__ == "__main__":
    inp = get_dataset(__file__) or sample
    inp = inp.split()
    n, m = int(inp[0]), int(inp[1])

    n_fact = factorial(n)
    res = 0
    for k in range(m, n + 1):
        res += n_fact // (factorial(k) * factorial(n - k))
    print(res % int(1e6))

    # C(n, k) = n! / (k! * (n-k)!)
