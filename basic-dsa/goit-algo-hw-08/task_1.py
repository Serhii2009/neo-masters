from avl_tree import AVLNode, build_tree, print_tree


# In a binary search tree every key of the left subtree is smaller than the key
# of its parent, so the smallest value is stored in the leftmost node.
# The descent takes O(h) steps, which is O(log n) for a balanced AVL tree.
def find_min(root: AVLNode):
    if root is None:
        return None

    current = root

    while current.left is not None:
        current = current.left

    return current.key


def main() -> None:
    values = [42, 17, 68, 5, 23, 55, 91, 3, 12, 78]
    root = build_tree(values)

    print("AVL tree built from:", values)
    print_tree(root)

    minimum = find_min(root)
    print(f"\nSmallest value in the tree: {minimum}")
    print(f"Expected (min of the inserted values): {min(values)}")

    print(f"\nSmallest value in an empty tree: {find_min(None)}")


main()
