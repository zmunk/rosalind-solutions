# from lexf import words
from utils import get_dataset


def words(chars, max_length):
    if max_length == 0:
        return []

    suffices = words(chars, max_length - 1)
    res = []
    for c in chars:
        res.append(c)
        for suffix in suffices:
            res.append(c + suffix)
    return res


sample = """
D N A
3
""".strip()

if __name__ == "__main__":
    inp = (get_dataset(__file__) or sample).split("\n")
    assert len(inp) == 2
    chars = inp[0].split()
    n = int(inp[1])

    for word in words(chars, n):
        print(word)
