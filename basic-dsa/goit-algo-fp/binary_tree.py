import uuid

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb

DEFAULT_COLOR = "skyblue"


class Node:
    def __init__(self, key, color=DEFAULT_COLOR):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node: Node, pos: dict, x: float = 0, y: float = 0, layer: int = 1):
    if node is None:
        return graph

    graph.add_node(node.id, color=node.color, label=node.val)

    if node.left:
        graph.add_edge(node.id, node.left.id)
        left = x - 1 / 2 ** layer
        pos[node.left.id] = (left, y - 1)
        add_edges(graph, node.left, pos, x=left, y=y - 1, layer=layer + 1)

    if node.right:
        graph.add_edge(node.id, node.right.id)
        right = x + 1 / 2 ** layer
        pos[node.right.id] = (right, y - 1)
        add_edges(graph, node.right, pos, x=right, y=y - 1, layer=layer + 1)

    return graph


def is_dark(color) -> bool:
    red, green, blue = to_rgb(color)
    return 0.299 * red + 0.587 * green + 0.114 * blue < 0.5


def build_heap_tree(heap: list) -> Node:
    if not heap:
        return None

    nodes = [Node(value) for value in heap]

    for index, node in enumerate(nodes):
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(nodes):
            node.left = nodes[left]

        if right < len(nodes):
            node.right = nodes[right]

    return nodes[0]


def draw_tree(root: Node, title: str = "", file_name: str = None) -> None:
    if root is None:
        print("Nothing to draw, the tree is empty.")
        return

    tree = nx.DiGraph()
    pos = {root.id: (0, 0)}
    tree = add_edges(tree, root, pos)

    colors = [data["color"] for _, data in tree.nodes(data=True)]
    labels = {node: data["label"] for node, data in tree.nodes(data=True)}
    dark = {node: label for node, label in labels.items()
            if is_dark(tree.nodes[node]["color"])}
    light = {node: label for node, label in labels.items() if node not in dark}

    plt.figure(figsize=(11, 6))

    if title:
        plt.title(title, fontsize=13)

    nx.draw_networkx_edges(tree, pos=pos, arrows=False, edge_color="#909090")
    nx.draw_networkx_nodes(tree, pos=pos, node_size=1800, node_color=colors,
                           edgecolors="#606060", linewidths=0.8)
    nx.draw_networkx_labels(tree, pos=pos, labels=dark, font_color="white", font_size=10)
    nx.draw_networkx_labels(tree, pos=pos, labels=light, font_color="black", font_size=10)

    plt.axis("off")
    plt.tight_layout()

    if file_name:
        plt.savefig(file_name, dpi=120)
        print(f"Image saved to {file_name}")

    plt.show()
