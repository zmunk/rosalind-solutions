from utils import parse_dataset, get_dataset

sample = """
>Rosalind_87
CAGCATGGTATCACAGCAGAG
""".strip()

if __name__ == "__main__":
    s = parse_dataset(get_dataset(__file__) or sample)[0]

    res = [0] * len(s)

    for i in range(1, len(s)):
        j = 0
        while s[i + j] == s[j]:
            res[i + j] = max(res[i + j], j + 1)
            j += 1

    # print(res)
    print(" ".join(map(str, res)))
