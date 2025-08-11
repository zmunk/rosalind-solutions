import sys
from pathlib import Path


def get_dataset(filename) -> str | None:
    """
    usage: `inp = get_dataset(__file__) or sample`

    this function returns None if `--dataset` argument is not passed
    when running the script
    """
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
parse_dataset = parse_fasta
