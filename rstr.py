from utils import get_dataset


def get_prob(s, gcc):
    # probability of getting 'G' or 'C'
    prob_gc = gcc / 2

    # probability of getting 'A' or 'T'
    prob_at = (1 - gcc) / 2

    # the probability that s is formed
    acc = 1

    for c in s:
        if c in "AT":
            acc *= prob_at
        else:
            acc *= prob_gc
    return acc


def main(s, num_samples, gcc):
    # the probability of getting s for a single string
    same_prob = get_prob(s, gcc)

    # the probability of getting anything other than s
    # for a single string
    diff_prob = 1 - same_prob

    # the probability that s is never formed
    acc = 1
    for _ in range(num_samples):
        acc *= diff_prob

    return format(1 - acc, ".3f")


sample = """
90000 0.6
ATAGCCGA
""".strip()

if __name__ == "__main__":
    inp = get_dataset(__file__) or sample
    line0, s = inp.split("\n")
    line0 = line0.split()
    num_samples = int(line0[0])
    gcc = float(line0[1])

    print(main(s, num_samples, gcc))
