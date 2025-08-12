from utils import get_dataset, parse_fasta


sample = """
>Rosalind_9499
TTTCCATTTA
>Rosalind_0942
GATTCATTTC
>Rosalind_6568
TTTCCATTTT
>Rosalind_1833
GTTCCATTTA
""".strip()


def expand(s):
    """
    expand each character to a vector
    where A: [1, 0, 0, 0]
          C: [0, 1, 0, 0]
          G: [0, 0, 1, 0]
          T: [0, 0, 0, 1]
    """
    res = []
    for c in s:
        match c:
            case "A":
                res.append([1, 0, 0, 0])
            case "C":
                res.append([0, 1, 0, 0])
            case "G":
                res.append([0, 0, 1, 0])
            case "T":
                res.append([0, 0, 0, 1])
    return res


def multiply(a, b):
    """
    sum of element-wise multiplication of all values
    i.e. a[0][0] * b[0][0] + a[0][1] * b[0][1] + ...
    """
    res = 0
    for row_a, row_b in zip(a, b):
        for aa, bb in zip(row_a, row_b):
            res += aa * bb
    return res


if __name__ == "__main__":
    inp = parse_fasta(get_dataset(__file__) or sample)
    string_len = len(inp[0])
    sz = len(inp)

    strings = list(map(expand, inp))
    matrix = [[0.0] * sz for _ in range(sz)]

    def coords():
        for i in range(len(inp)):
            for j in range(i + 1, len(inp)):
                yield i, j

    for i, j in coords():
        diff = (string_len - multiply(strings[i], strings[j])) / string_len
        matrix[i][j] = diff
        matrix[j][i] = diff

    def fmt(s):
        return format(s, ".5f")

    for row in matrix:
        print(" ".join(list(map(fmt, row))))
