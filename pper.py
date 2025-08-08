import sys
from splc import get_dataset, parse_dataset

if "--dataset" in sys.argv:
    inp = get_dataset(__file__)
    n, k = list(map(int, inp.split(" ")))

else:
    n, k = 21, 7

res = 1
for i in range(n, n - k, -1):
    res = (res * i) % int(1e6)
print(res)
