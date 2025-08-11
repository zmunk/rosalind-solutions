import re
import requests
from utils import get_dataset, parse_fasta


def get_fasta(entry_id):
    genbank_url = f"https://www.ncbi.nlm.nih.gov/nuccore/{entry_id}.1?report=fasta"
    res = requests.get(genbank_url)
    assert res.status_code == 200
    assert (m := re.search(r"ncbi_uid=(\d+)", res.text))
    ncbi_uid = m.group(1)
    fasta_url = (
        "https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?"
        + "id="
        + ncbi_uid
        + "&db=nuccore&report=fasta&extrafeat=null&conwithfeat=on&hide-cdd=on&retmode=html&ncbi_phid=0&withmarkup=on&tool=portal&log$=seqview&maxdownloadsize=1000000"
    )
    res = requests.get(fasta_url)
    assert res.status_code == 200
    return res.text.strip()


sample = "FJ817486 JX069768 JX469983"


if __name__ == "__main__":
    inp = (get_dataset(__file__) or sample).split()
    min_len = float("inf")
    shortest = None
    for entry_id in inp:
        fasta = get_fasta(entry_id)
        s = parse_fasta(fasta)[0]
        if len(s) < min_len:
            shortest = fasta
            min_len = len(s)
    assert shortest
    print(shortest)
