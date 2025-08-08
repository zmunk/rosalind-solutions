import re
import json
from pathlib import Path

raw = """
UUU F      CUU L      AUU I      GUU V
UUC F      CUC L      AUC I      GUC V
UUA L      CUA L      AUA I      GUA V
UUG L      CUG L      AUG M      GUG V
UCU S      CCU P      ACU T      GCU A
UCC S      CCC P      ACC T      GCC A
UCA S      CCA P      ACA T      GCA A
UCG S      CCG P      ACG T      GCG A
UAU Y      CAU H      AAU N      GAU D
UAC Y      CAC H      AAC N      GAC D
UAA Stop   CAA Q      AAA K      GAA E
UAG Stop   CAG Q      AAG K      GAG E
UGU C      CGU R      AGU S      GGU G
UGC C      CGC R      AGC S      GGC G
UGA Stop   CGA R      AGA R      GGA G
UGG W      CGG R      AGG R      GGG G 
"""

p = Path("data/codon.json")

if p.exists():
    aa_dict = json.load(open(p))
else:
    regex = re.compile("^" + r"(\S{3} \S+) *" * 4)
    aa_dict = {}
    for line in raw.strip().split("\n"):
        m = regex.match(line)
        assert m
        for pair in m.groups():
            codon, aa = pair.split(" ")
            aa_dict[codon] = aa
    with open(p, "w") as f:
        json.dump(aa_dict, f, indent=4)
