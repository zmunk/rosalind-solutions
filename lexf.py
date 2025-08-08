import sys
from splc import get_dataset


def words(chars, length):
    if length == 0:
        return [""]

    suffices = words(chars, length - 1)
    res = []
    for c in chars:
        for suffix in suffices:
            res.append(c + suffix)
    return res


sample = """
A C G T
2
""".strip()

if __name__ == "__main__":
    if "--dataset" in sys.argv:
        inp = get_dataset(__file__)
        # print(inp)
        # exit()
    else:
        inp = sample

    inp = inp.split("\n")
    chars = inp[0].split(" ")
    n = int(inp[1])

    for word in words(chars, n):
        print(word)
