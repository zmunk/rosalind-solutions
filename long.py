import sys
from splc import get_dataset, parse_dataset

sample = """
>Rosalind_56
ATTAGACCTG
>Rosalind_57
CCTGCCGGAA
>Rosalind_58
AGACCTGCCG
>Rosalind_59
GCCGGAATAC
""".strip()

if __name__ == "__main__":
    if "--dataset" in sys.argv:
        inp = get_dataset(__file__)
        strings = parse_dataset(inp)
    else:
        strings = sample.split("\n")[1::2]

    # find shortest unique prefix length
    prefix_len = 0
    d = {}  # prefix -> full string
    while len(d) < len(strings):
        prefix_len += 1
        # print("prefix_len:", prefix_len)
        d = {}
        for s in strings:
            if s[:prefix_len] in d:
                break
            d[s[:prefix_len]] = s
    # print("FOUND", "prefix_len:", prefix_len)

    while len(d) > 1:
        for s in list(d.values()):
            for i in range(1, len(s) - 1):
                right_prefix = s[i : i + prefix_len]
                if right_prefix not in d:
                    continue
                right = d[right_prefix]
                overlap = s[i:]
                if not right.startswith(overlap):
                    continue
                left_prefix = s[:prefix_len]
                left_unique = s[:i]
                d[left_prefix] = left_unique + right
                del d[right_prefix]
                break
    print(list(d.values())[0])
