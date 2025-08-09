from utils import get_dataset

if __name__ == "__main__":
    inp = (get_dataset(__file__) or "21 7").split()
    n, k = int(inp[0]), int(inp[1])

    res = 1
    for i in range(n, n - k, -1):
        res = (res * i) % int(1e6)
    print(res)
