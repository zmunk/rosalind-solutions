from utils import parse_dataset, get_dataset


def longest_common_subsequence_length(text1, text2) -> int:
    i_max = len(text1) - 1
    j_max = len(text2) - 1

    def coords():
        for coord_sum in range(i_max + j_max, -1, -1):
            for i in range(min(coord_sum, i_max), -1, -1):
                j = coord_sum - i
                if j > j_max:
                    break
                yield i, j

    # longest subsequence lengths
    lengths = [[0] * (len(text2) + 1) for _ in range(len(text1) + 1)]
    # longest subsequences
    seqs = {}
    for i, j in coords():
        if text1[i] == text2[j]:
            length = 1 + lengths[i + 1][j + 1]
            seq = text1[i] + seqs.get((i + 1, j + 1), "")
        elif lengths[i + 1][j] > lengths[i][j + 1]:
            length = lengths[i + 1][j]
            seq = seqs.get((i + 1, j), "")
        else:
            length = lengths[i][j + 1]
            seq = seqs.get((i, j + 1), "")
        lengths[i][j] = length
        seqs[(i, j)] = seq

    # for row in lengths:
    #     print(row)

    return seqs[(0, 0)]


sample = """
>Rosalind_23
AACCTTGG
>Rosalind_64
ACACTGTGA
""".strip()

if __name__ == "__main__":
    a, b = parse_dataset(get_dataset(__file__) or sample)
    print(longest_common_subsequence_length(a, b))
