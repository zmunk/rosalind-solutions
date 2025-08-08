import sys
from itertools import permutations

if __name__ == "__main__":
    if "--dataset" in sys.argv:
        n = int(open("input/rosalind_perm.txt").read().strip())
    else:
        n = 3
    perms = list(permutations(range(1, n + 1)))
    print(len(perms))
    for perm in perms:
        print(" ".join(map(str, perm)))
