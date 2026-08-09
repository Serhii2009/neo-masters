class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None


def get_height(node: AVLNode) -> int:
    return node.height if node else 0


def get_balance(node: AVLNode) -> int:
    return get_height(node.left) - get_height(node.right) if node else 0


def update_height(node: AVLNode) -> None:
    node.height = 1 + max(get_height(node.left), get_height(node.right))


def rotate_right(node: AVLNode) -> AVLNode:
    new_root = node.left
    node.left = new_root.right
    new_root.right = node

    update_height(node)
    update_height(new_root)
    return new_root


def rotate_left(node: AVLNode) -> AVLNode:
    new_root = node.right
    node.right = new_root.left
    new_root.left = node

    update_height(node)
    update_height(new_root)
    return new_root


def insert(root: AVLNode, key) -> AVLNode:
    if root is None:
        return AVLNode(key)

    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    else:
        return root

    update_height(root)
    balance = get_balance(root)

    if balance > 1:
        if key > root.left.key:
            root.left = rotate_left(root.left)
        return rotate_right(root)

    if balance < -1:
        if key < root.right.key:
            root.right = rotate_right(root.right)
        return rotate_left(root)

    return root


def build_tree(values: list) -> AVLNode:
    root = None

    for value in values:
        root = insert(root, value)

    return root


def print_tree(node: AVLNode, level: int = 0, prefix: str = "Root:") -> None:
    if node is None:
        return

    print(" " * (level * 4) + f"{prefix} {node.key}")
    print_tree(node.left, level + 1, "L---")
    print_tree(node.right, level + 1, "R---")
