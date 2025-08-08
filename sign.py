import sys
from splc import get_dataset


def signed_permutations(arr) -> list[list]:
    if len(arr) == 0:
        return [[]]

    res = []
    for i in range(len(arr)):
        n = arr[i]
        for perm in signed_permutations(arr[:i] + arr[i + 1 :]):
            res.append([n] + perm)
            if n != 0:
                res.append([-n] + perm)
    return res


sample = "2"
if __name__ == "__main__":
    if "--dataset" in sys.argv:
        inp = get_dataset(__file__)
    else:
        inp = sample

    inp = int(inp)
    perms = signed_permutations(list(range(1, inp + 1)))
    print(len(perms))
    for perm in perms:
        print(" ".join(map(str, perm)))
    # print(perms)
    # print("\n".join(map(lambda p: f"{p[0]} {p[1]}", perms)))
