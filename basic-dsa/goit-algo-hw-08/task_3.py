import heapq


# The cost of one connection is the sum of the two lengths, and the result stays
# in the pool, so every cable is paid for again in each of the following
# connections. To keep the total minimal the longest cables have to take part in
# as few connections as possible, which means that on every step the two
# currently shortest cables must be joined. A min-heap gives both of them in
# O(log n), so the whole algorithm runs in O(n log n).
def minimum_connection_cost(lengths: list) -> tuple:
    if len(lengths) < 2:
        return 0, []

    heap = list(lengths)
    heapq.heapify(heap)

    total_cost = 0
    steps = []

    while len(heap) > 1:
        first = heapq.heappop(heap)
        second = heapq.heappop(heap)
        cost = first + second

        total_cost += cost
        steps.append((first, second, cost))
        heapq.heappush(heap, cost)

    return total_cost, steps


# The opposite strategy, joining the two longest cables first, is used only to
# show how much the order of connections influences the total cost.
def maximum_connection_cost(lengths: list) -> int:
    if len(lengths) < 2:
        return 0

    heap = [-length for length in lengths]
    heapq.heapify(heap)

    total_cost = 0

    while len(heap) > 1:
        first = -heapq.heappop(heap)
        second = -heapq.heappop(heap)
        cost = first + second

        total_cost += cost
        heapq.heappush(heap, -cost)

    return total_cost


def report(lengths: list) -> None:
    print(f"Cables: {lengths}")

    total_cost, steps = minimum_connection_cost(lengths)

    for first, second, cost in steps:
        print(f"  connect {first} + {second} = {cost}")

    print(f"Minimum total cost: {total_cost}")

    if len(lengths) > 1:
        print(f"Most expensive order, for comparison: {maximum_connection_cost(lengths)}")

    print()


def main() -> None:
    report([8, 4, 6, 12])
    report([20, 4, 8, 2, 1, 7])
    report([5, 5, 5, 5])
    report([100])
    report([])


main()
