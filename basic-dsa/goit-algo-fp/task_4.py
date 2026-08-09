import heapq
from pathlib import Path

from binary_tree import build_heap_tree, draw_tree

VALUES = [12, 7, 25, 3, 19, 5, 30, 1, 8, 14, 22]


def is_valid_min_heap(heap: list) -> bool:
    for index in range(len(heap)):
        for child in (2 * index + 1, 2 * index + 2):
            if child < len(heap) and heap[index] > heap[child]:
                return False

    return True


def describe(heap: list) -> None:
    print("Parent and children by index")
    header = f"{'Index':<7}| {'Value':<7}| {'Left':<12}| Right"
    print(header)
    print("-" * len(header))

    for index, value in enumerate(heap):
        left = 2 * index + 1
        right = 2 * index + 2
        left_text = f"{heap[left]} (i={left})" if left < len(heap) else "-"
        right_text = f"{heap[right]} (i={right})" if right < len(heap) else "-"
        print(f"{index:<7}| {value:<7}| {left_text:<12}| {right_text}")


def main() -> None:
    heap = list(VALUES)
    heapq.heapify(heap)

    print("Source values:", VALUES)
    print("Heap array:   ", heap)
    print("Min-heap property holds:", is_valid_min_heap(heap))
    print()

    describe(heap)

    output = Path(__file__).parent / "heap_tree.png"
    draw_tree(build_heap_tree(heap), f"Binary min-heap, {len(heap)} nodes", str(output))


main()
