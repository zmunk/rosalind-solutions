import sys
from splc import get_dataset, parse_dataset

sample = """
10
1 2
2 8
4 10
5 9
6 10
7 9
""".strip()

if __name__ == "__main__":
    if "--dataset" in sys.argv:
        inp = get_dataset(__file__)
    else:
        inp = sample

    inp = inp.split("\n")
    n_nodes = int(inp[0])
    print(n_nodes - len(inp))
# nodes = list(range(0, n_nodes + 1))
#
#
# # nodes = list(range(1, n_nodes + 1))
# # print(nodes)
# def root(node):
#     while nodes[node] != node:
#         node = nodes[node]
#     return node
#
#
# for line in inp[-1:0:-1]:
#     # for line in inp[1:]:
#     a, b = map(int, line.split())
#
#     a = root(a)
#     b = root(b)
#     # print(a, b)
#
#     a, b = min(a, b), max(a, b)
#
#     nodes[b] = a
#     # print(nodes)
#
# roots = set()
# for node in nodes[1:]:
#     roots.add(root(node))
# # print(roots)
# print(len(roots) - 1)
#
# # for i, node in enumerate(nodes):
# #     if i + 1 == node:
# #         print(i + 1)
# #         continue
# #     curr = node
# #     while nodes[curr - 1] != curr:
# #         curr = nodes[curr - 1]
# #     print(i + 1, "->", curr)
