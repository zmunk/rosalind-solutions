from functools import cache
from utils import get_dataset, parse_fasta
from revp import complement_rna_dict


sample = """
>Rosalind_57
AUAU
""".strip()


@cache
def num_matchings(s):
    if len(s) in [0, 1]:
        return 1

    res = 0
    matching_base = complement_rna_dict[s[0]]

    # including first base
    for i in range(1, len(s)):
        if s[i] == matching_base:
            res += num_matchings(s[1:i]) * num_matchings(s[i + 1 :])

    # excluding first base
    res += num_matchings(s[1:])

    return res


if __name__ == "__main__":
    inp = parse_fasta(get_dataset(__file__) or sample)
    print(num_matchings(inp[0]) % int(1e6))
