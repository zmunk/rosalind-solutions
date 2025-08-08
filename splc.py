from pathlib import Path
from orf import get_codons, get_rna
from codonlib import aa_dict


def remove_intron(dna, intron):
    l = len(intron)
    res = ""
    while True:
        try:
            i = dna.index(intron)
        except ValueError:
            res += dna
            break
        else:
            # print(" " * i + dna[i : i + l])
            res += dna[:i]
            dna = dna[i + l :]
    return res


def convert_dna_to_protein(dna):
    rna = get_rna(dna)
    res = ""
    for codon in get_codons(rna):
        if aa_dict[codon] == "Stop":
            break
        res += aa_dict[codon]
    return res


def parse_dataset(data):
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


def get_dataset(filename):
    file_id = Path(filename).stem
    return open(Path(f"~/Downloads/rosalind_{file_id}.txt").expanduser()).read().strip()


sample = """
>Rosalind_10
ATGGTCTACATAGCTGACAAACAGCACGTAGCAATCGGTCGAATCTCGAGAGGCATATGGTCACATGATCGGTCGAGCGTGTTTCAAAGTTTGCGCCTAG
>Rosalind_12
ATCGGTCGAA
>Rosalind_15
ATCGGTCGAGCGTGT
""".strip()


def main(inp):
    strings = parse_dataset(inp)
    dna = strings[0]
    for intron in strings[1:]:
        dna = remove_intron(dna, intron)
    return convert_dna_to_protein(dna)


if __name__ == "__main__":
    assert main(sample) == "MVYIADKQHVASREAYGHMFKVCA"
    print(main(get_dataset(__file__)))
