import sys
from utils import get_dataset

complement_dna_dict = {
    "A": "T",
    "T": "A",
    "G": "C",
    "C": "G",
}

complement_rna_dict = {
    "A": "U",
    "U": "A",
    "G": "C",
    "C": "G",
}


def complement_dna(s):
    """
    Complement of DNA string.
    """
    return "".join(map(lambda x: complement_dna_dict[x], s))


def complement_rna(s):
    """
    Complement of RNA string.
    """
    return "".join(map(lambda x: complement_rna_dict[x], s))


sample = """
>
TCAATGCATGCGGGTCTATATGCAT
""".strip()


def format_dataset(raw):
    return "".join(raw.split("\n")[1:])


if __name__ == "__main__":
    debugging = "--debug" in sys.argv
    s = format_dataset(get_dataset(__file__) or sample)
    for i in range(1, len(s) - 2):
        left = i
        right = i + 1
        while (
            left >= 0
            and right < len(s)
            and right - left + 1 <= 12
            and s[left] == complement_dna_dict[s[right]]
        ):
            if right - left + 1 >= 4:
                print(left + 1, right - left + 1)
                if debugging:
                    print("  ", s[left : right + 1])
                    print("  ", complement_dna(s[left : right + 1]))
            left -= 1
            right += 1
