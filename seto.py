from utils import get_dataset


sample = """
10
{1, 2, 3, 4, 5}
{2, 8, 5, 10}
""".strip()

if __name__ == "__main__":
    inp = get_dataset(__file__) or sample
    n, a, b = inp.split("\n")
    n = int(n)
    a = set(map(int, a[1:-1].split(", ")))
    b = set(map(int, b[1:-1].split(", ")))
    print(a | b)
    print(a & b)
    print(a - b)
    print(b - a)
    univ = {i for i in range(1, n + 1)}
    print(univ - a)
    print(univ - b)
