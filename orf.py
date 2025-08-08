import sys
from codonlib import aa_dict

def cyan_bold(s):
    return f'\033[1;36m{s}\033[0m'

def red_bold(s):
    return f'\033[1;31m{s}\033[0m'

def get_codons(s):
    for i in range(0, len(s), 3):
        if i + 3 > len(s):
            return
        yield s[i:i+3]

start_codon = "AUG"

def rev_comp(s):
    res = ""
    for c in s[::-1]:
        match c:
            case "C":
                res += "G"
            case "G":
                res += "C"
            case "A":
                res += "U"
            case "U":
                res += "A"
    return res


def get_rna(s):
    s_rna = ""
    for c in s:
        if c == "T":
            s_rna += "U"
        else:
            s_rna += c
    return s_rna

def get_frames(s_rna):
    frames = []
    for offset in range(3):
        rna_codons = list(get_codons(s_rna[offset:]))
        start_locs = []
        for i, codon in enumerate(rna_codons):
            if codon == start_codon:
                start_locs.append(i)
        for start_loc in start_locs:
            curr = ""
            for codon in rna_codons[start_loc:]:
                if aa_dict[codon] == "Stop":
                    frames.append(curr)
                    break
                curr += aa_dict[codon]
    return frames

def display(s_rna, oneline=False):
    res = []
    for codon in get_codons(s_rna):
        if aa_dict[codon] == "Stop":
            codon = red_bold(codon)
        elif codon == start_codon:
            codon = cyan_bold(codon)
        res.append(codon)
    if oneline:
        print(" ".join(res))
    else:
        print("\n".join(res))

if __name__ == "__main__":
    if "--dataset" in sys.argv:
        s = "".join(open("input/rosalind_orf.txt").read().strip().split("\n")[1:])
    else:
        s = "AGCCATGTAGCTAACTCAGGTTACATGGGGATGACCCCGCGACTTGGATTAGAGTCTCTTTTGGAATAAGCCTGAATGATCCGAGTAGCATCTCAG"
    s = get_rna(s)
    frames = set(get_frames(s)) | set(get_frames(rev_comp(s)))
    for f in frames:
        print(f)
