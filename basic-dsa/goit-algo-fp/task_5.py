import heapq
from pathlib import Path
from collections import deque

from binary_tree import Node, build_heap_tree, draw_tree

VALUES = [12, 7, 25, 3, 19, 5, 30, 1, 8, 14, 22]

DARK = (10, 42, 92)
LIGHT = (176, 226, 255)


def generate_colors(count: int) -> list:
    if count <= 0:
        return []

    if count == 1:
        return ["#{:02X}{:02X}{:02X}".format(*LIGHT)]

    colors = []

    for index in range(count):
        ratio = index / (count - 1)
        channels = tuple(round(dark + (light - dark) * ratio)
                         for dark, light in zip(DARK, LIGHT))
        colors.append("#{:02X}{:02X}{:02X}".format(*channels))

    return colors


def depth_first_order(root: Node) -> list:
    if root is None:
        return []

    order = []
    stack = [root]

    while stack:
        node = stack.pop()
        order.append(node)

        if node.right is not None:
            stack.append(node.right)

        if node.left is not None:
            stack.append(node.left)

    return order


def breadth_first_order(root: Node) -> list:
    if root is None:
        return []

    order = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        order.append(node)

        if node.left is not None:
            queue.append(node.left)

        if node.right is not None:
            queue.append(node.right)

    return order


def paint(order: list) -> None:
    for node, color in zip(order, generate_colors(len(order))):
        node.color = color


def show(title: str, traversal, heap: list, file_name: Path) -> None:
    root = build_heap_tree(heap)
    order = traversal(root)
    paint(order)

    print(f"{title}: " + " -> ".join(str(node.val) for node in order))
    print("  colours: " + " ".join(node.color for node in order))

    draw_tree(root, f"{title}, from dark to light in visiting order", str(file_name))


def main() -> None:
    heap = list(VALUES)
    heapq.heapify(heap)
    print("Heap array:", heap, "\n")

    folder = Path(__file__).parent

    show("Depth first search", depth_first_order, heap, folder / "dfs_traversal.png")
    print()
    show("Breadth first search", breadth_first_order, heap, folder / "bfs_traversal.png")


main()
