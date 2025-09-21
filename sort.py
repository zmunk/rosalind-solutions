from utils import get_dataset
from rear import get_optimal_steps, interactive


sample = """
1 2 3 4 5 6 7 8 9 10
1 8 9 3 2 7 6 5 4 10
""".strip()

if __name__ == "__main__":
    inp = get_dataset(__file__) or sample
    a, b = inp.split("\n")
    a = a.split()
    b = b.split()

    # interactive(b, a)

    # NOTE: to go from a -> b, b must be the first argument and a is the second
    swaps, _ = get_optimal_steps(b, a)
    print(len(swaps))
    for left, right in swaps:
        print(left + 1, right + 1)
