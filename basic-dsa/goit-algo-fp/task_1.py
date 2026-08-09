class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self, values: list = None):
        self.head = None
        self.tail = None

        for value in values or []:
            self.append(value)

    def append(self, value) -> None:
        node = Node(value)

        if self.head is None:
            self.head = node
        else:
            self.tail.next = node

        self.tail = node

    def to_list(self) -> list:
        values = []
        current = self.head

        while current is not None:
            values.append(current.value)
            current = current.next

        return values

    def refresh_tail(self) -> None:
        current = self.head

        while current is not None and current.next is not None:
            current = current.next

        self.tail = current

    def reverse(self) -> None:
        previous = None
        current = self.head
        self.tail = self.head

        while current is not None:
            following = current.next
            current.next = previous
            previous = current
            current = following

        self.head = previous

    def sort(self) -> None:
        self.head = merge_sort(self.head)
        self.refresh_tail()

    def __str__(self):
        values = self.to_list()
        return " -> ".join(str(value) for value in values) if values else "(empty)"


def split(head: Node) -> tuple:
    slow = head
    fast = head.next

    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next

    second = slow.next
    slow.next = None
    return head, second


def merge_nodes(first: Node, second: Node) -> Node:
    guard = Node(None)
    tail = guard

    while first is not None and second is not None:
        if first.value <= second.value:
            tail.next = first
            first = first.next
        else:
            tail.next = second
            second = second.next

        tail = tail.next

    tail.next = first if first is not None else second
    return guard.next


def merge_sort(head: Node) -> Node:
    if head is None or head.next is None:
        return head

    left, right = split(head)
    return merge_nodes(merge_sort(left), merge_sort(right))


def merge_sorted_lists(first: LinkedList, second: LinkedList) -> LinkedList:
    merged = LinkedList()
    merged.head = merge_nodes(first.head, second.head)
    merged.refresh_tail()

    first.head = first.tail = None
    second.head = second.tail = None
    return merged


def main() -> None:
    print("Reversing")
    numbers = LinkedList([1, 2, 3, 4, 5, 6])
    print(f"  before: {numbers}")
    numbers.reverse()
    print(f"  after:  {numbers}")
    print(f"  head: {numbers.head.value}, tail: {numbers.tail.value}")

    print("\nSorting")
    unsorted = LinkedList([42, 7, 19, 3, 25, 11, 8, 30, 1])
    print(f"  before: {unsorted}")
    unsorted.sort()
    print(f"  after:  {unsorted}")

    print("\nMerging two sorted lists")
    first = LinkedList([1, 4, 7, 10, 15])
    second = LinkedList([2, 3, 8, 12])
    print(f"  first:  {first}")
    print(f"  second: {second}")
    merged = merge_sorted_lists(first, second)
    print(f"  merged: {merged}")

    print("\nEdge cases")
    empty = LinkedList()
    empty.reverse()
    empty.sort()
    print(f"  empty list after reverse and sort: {empty}")
    print(f"  merging an empty list with [5, 9]: "
          f"{merge_sorted_lists(LinkedList(), LinkedList([5, 9]))}")


main()
