from utils import get_dataset, parse_fasta


sample = """
3
""".strip()

if __name__ == "__main__":
    inp = get_dataset(__file__) or sample
    print(2 ** int(inp) % int(1e6))
