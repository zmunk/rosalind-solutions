from utils import get_dataset


def count_nodes(num_leaves):
    if num_leaves == 1:
        return 1
    if num_leaves % 2 == 1:
        return 2 + count_nodes(num_leaves - 1)
    return num_leaves + count_nodes(num_leaves // 2)


def main(n):
    return count_nodes(n) - n - 1


if __name__ == "__main__":
    assert main(4) == 2
    if dataset := get_dataset(__file__):
        print(main(int(dataset)))
