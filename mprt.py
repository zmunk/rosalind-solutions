import sys
from pathlib import Path
import requests

def get_seq(uid):
    p = Path(f"data/{uid}")
    if p.exists():
        with open(p) as f:
            seq = f.read()
    else:

        url = f"https://rest.uniprot.org/uniprotkb/{uid}.fasta"
        response = requests.get(url)
        assert response.status_code == 200, f"Status: {response.status_code}"
        lines = response.text.strip().split('\n')[1:]
        seq = "".join(lines)

        with open(p, "w") as f:
            f.write(seq)

    return seq


def step(seq, locs, cond):
    res = []
    for loc in locs:
        if cond(seq[loc + 1]):
            res.append(loc + 1)
    return res


# N{P}[ST]{P}
conditions = [
    lambda x: x == "N",
    lambda x: x != "P",
    lambda x: x in "ST",
    lambda x: x != "P",
]

def main(uid):
    seq = get_seq(uid.split("_", 1)[0])
    locs = step(seq, range(-1, len(seq) - 1), conditions[0])
    for cond in conditions[1:]:
        locs = step(seq, locs, cond)
    return list(map(lambda x: x - 2, locs))

sample = """ 
A2Z669
B5ZC00
P07204_TRBM_HUMAN
P20840_SAG1_YEAST
""".strip()

if __name__ == "__main__":
    if "--dataset" in sys.argv:
        inp = open("input/rosalind_mprt.txt").read().strip().split("\n")
    else:
        inp = sample.split("\n")
    for uid in inp:
        try:
            res = main(uid)
        except Exception:
            continue
        else:
            if len(res) > 0:
                print(uid)
                print(" ".join(map(str, res)))

