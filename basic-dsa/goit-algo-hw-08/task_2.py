from avl_tree import AVLNode, build_tree, print_tree


# Every node has to be visited exactly once, so the traversal order does not
# matter and the complexity is O(n).
def sum_values(root: AVLNode) -> int:
    if root is None:
        return 0

    return root.key + sum_values(root.left) + sum_values(root.right)


def main() -> None:
    values = [42, 17, 68, 5, 23, 55, 91, 3, 12, 78]
    root = build_tree(values)

    print("AVL tree built from:", values)
    print_tree(root)

    total = sum_values(root)
    print(f"\nSum of all values in the tree: {total}")
    print(f"Expected (sum of the inserted values): {sum(values)}")

    print(f"\nSum of an empty tree: {sum_values(None)}")


main()
