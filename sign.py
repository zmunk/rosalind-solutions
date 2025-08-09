from utils import get_dataset


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


if __name__ == "__main__":
    inp = int(get_dataset(__file__) or "2")
    perms = signed_permutations(list(range(1, inp + 1)))
    print(len(perms))
    for perm in perms:
        print(" ".join(map(str, perm)))
