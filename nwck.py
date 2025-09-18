import string
from collections import deque
from lgis import cyan
from utils import get_dataset


sample = """
(cat)dog;
dog cat

(dog,cat);
dog cat
""".strip()


def parse(inp):
    lines = iter(inp.split("\n"))
    curr = []
    while True:
        try:
            while (line := next(lines)) != "":
                curr.append(line)
        except StopIteration:
            yield curr
            return

        yield curr
        curr = []


class Node:
    def __init__(self, name=""):
        self.name: str = name
        self.children: list[Node] = []
        self.parent = None
        self.distance = None

    def set_children(self, children: list["Node"]):
        self.children = children
        for child in children:
            child.parent = self

    def get_edges(self):
        if self.parent is not None:
            yield self.parent
        yield from self.children

    def add_letter_to_name(self, letter: str):
        self.name = letter + self.name

    def __repr__(self) -> str:
        label = None
        if self.name:
            label = self.name

            if self.distance is not None:
                label = cyan(label + f" ({self.distance})")
        elif self.distance is not None:
            label = cyan(f"({self.distance})")

        if label is None:
            label = "o"

        res = [label]
        for i, child in enumerate(self.children):
            is_last = i == len(self.children) - 1
            lines = repr(child).split("\n")
            if is_last:
                res.append("└─ " + lines[0])
                for line in lines[1:]:
                    res.append("   " + line)
            else:
                res.append("├─ " + lines[0])
                for line in lines[1:]:
                    res.append("│  " + line)
        return "\n".join(res)


def create_tree(raw_tree):
    nodes_lookup = {}

    def add_node(node):
        nodes_lookup[node.name] = node

    def parse_newick(it):
        nodes = [Node()]
        for c in it:
            match c:
                case ")":
                    nodes[-1].set_children(parse_newick(it))
                case "(":
                    add_node(nodes[-1])
                    break
                case ",":
                    add_node(nodes[-1])
                    nodes.append(Node())
                case _:
                    assert c in string.ascii_letters + ":._-0123456789", c
                    nodes[-1].add_letter_to_name(c)
        return nodes

    it = iter(raw_tree[::-1])
    assert next(it) == ";"
    parse_newick(it)

    return nodes_lookup


def main(inp):
    res = []
    for raw_tree, node_pair in parse(inp):
        nodes = create_tree(raw_tree)
        start, end = node_pair.split()
        assert start in nodes, (start, nodes.keys())
        assert end in nodes, (end, nodes.keys())

        q = deque()
        q.append((nodes[start], 0))

        while q:
            node, dist = q.popleft()

            if node.distance is not None:
                continue

            node.distance = dist

            if node == nodes[end]:
                break

            for other_node in node.get_edges():
                q.append((other_node, dist + 1))

        distance = nodes[end].distance
        res.append(str(distance))

    return " ".join(res)


if __name__ == "__main__":
    inp = get_dataset(__file__) or sample
    print(main(inp))
