import re
import shutil
import subprocess
from pathlib import Path
from utils import get_dataset


def main(input_file):
    output_folder = Path("meme_output")
    if output_folder.exists():
        shutil.rmtree(output_folder)
    subprocess.run(
        ["meme", "-protein", input_file, "-o", str(output_folder)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    regex = re.compile("^Multilevel.*$")
    lines = iter(open(output_folder / "meme.txt").read().split("\n"))
    while not regex.match((line := next(lines))):
        continue
    assert (m := re.match(r"^(Multilevel\s+)", line))
    indent = len(m.group(1))

    seq = list(line[indent:])
    while (line := next(lines)).strip() != "":
        for i, c in enumerate(line[indent:]):
            if c == " ":
                continue
            seq[i] += c

    res = ""
    for c in seq:
        if len(c) == 1:
            res += c
        else:
            res += "[" + c + "]"

    shutil.rmtree(output_folder)

    return res


sample = """
>Rosalind_7142
PFTADSMDTSNMAQCRVEDLWWCWIPVHKNPHSFLKTWSPAAGHRGWQFDHNFFVYMMGQ
FYMTKYNHGYAPARRKRFMCQTFFILTFMHFCFRRAHSMVEWCPLTTVSQFDCTPCAIFE
WGFMMEFPCFRKQMHHQSYPPQNGLMNFNMTISWYQMKRQHICHMWAEVGILPVPMPFNM
SYQIWEKGMSMGCENNQKDNEVMIMCWTSDIKKDGPEIWWMYNLPHYLTATRIGLRLALY
>Rosalind_4494
VPHRVNREGFPVLDNTFHEQEHWWKEMHVYLDALCHCPEYLDGEKVYFNLYKQQISCERY
PIDHPSQEIGFGGKQHFTRTEFHTFKADWTWFWCEPTMQAQEIKIFDEQGTSKLRYWADF
QRMCEVPSGGCVGFEDSQYYENQWQREEYQCGRIKSFNKQYEHDLWWCWIPVHKKPHSFL
KTWSPAAGHRGWQFDHNFFSTKCSCIMSNCCQPPQQCGQYLTSVCWCCPEYEYVTKREEM
>Rosalind_3636
ETCYVSQLAYCRGPLLMNDGGYGPLLMNDGGYTISWYQAEEAFPLRWIFMMFWIDGHSCF
NKESPMLVTQHALRGNFWDMDTCFMPNTLNQLPVRIVEFAKELIKKEFCMNWICAPDPMA
GNSQFIHCKNCFHNCFRQVGMDLWWCWIPVHKNPHSFLKTWSPAAGHRGWQFDHNFFQMM
GHQDWGTQTFSCMHWVGWMGWVDCNYDARAHPEFYTIREYADITWYSDTSSNFRGRIGQN
""".strip()

if __name__ == "__main__":
    if get_dataset(__file__):
        file_id = Path(__file__).stem
        input_file = Path(f"~/Downloads/rosalind_{file_id}.txt").expanduser()
    else:
        input_file = Path("input/meme.txt")
        with open(input_file, "w") as f:
            f.write(sample)
    print(main(input_file))
