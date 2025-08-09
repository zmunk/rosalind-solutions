import sys
from pathlib import Path


def get_dataset(filename):
    if "--dataset" in sys.argv:
        file_id = Path(filename).stem
        return (
            open(Path(f"~/Downloads/rosalind_{file_id}.txt").expanduser())
            .read()
            .strip()
        )


def parse_fasta(data):
    lines = data.split("\n")
    res = []
    curr = ""
    for line in lines:
        if line[0] == ">":
            if len(curr) > 0:
                res.append(curr)
            curr = ""
            continue

        curr += line

    res.append(curr)
    return res


# alias
parse_database = parse_fasta
