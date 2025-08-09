from utils import get_dataset, parse_dataset
from functools import cache
from revp import complement_rna_dict


@cache
def cat(n) -> int:
    """
    c_n = S(k=1,n) c_(k-1) * c_(n-k)
    """
    if n in [0, 1]:
        return 1
    res = 0
    for k in range(1, n + 1):
        res += cat(k - 1) * cat(n - k)
    return res


def options(loop, target):
    a_count = 0
    g_count = 0
    for i, c in enumerate(loop):
        if c == target and a_count == 0 and g_count == 0:
            yield i

        match c:
            case "A":
                a_count += 1
            case "U":
                a_count -= 1
            case "G":
                g_count += 1
            case "C":
                g_count -= 1


@cache
def num_options(s):
    # def num_options(s, depth=0):
    if len(s) == 0:
        return 1

    res = 0
    c, s = s[0], s[1:]
    for i in options(s, complement_rna_dict[c]):
        # print(" " * depth, c, s[:i], s[i], s[i + 1 :])
        res += num_options(s[:i]) * num_options(s[i + 1 :])
        # res += num_options(s[:i], depth=depth + 1) * num_options(
        #     s[i + 1 :], depth=depth + 1
        # )

    return res


if __name__ == "__main__":
    inp = parse_dataset(get_dataset(__file__) or "UAGCGUGAUCAC")[0]
    print(num_options(inp) % int(1e6))
