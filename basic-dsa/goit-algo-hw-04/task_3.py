import random
import timeit

RUN_SIZE = 32
SIZES = [1_000, 5_000, 10_000]
LARGE_SIZES = [50_000, 100_000, 500_000]


def insertion_sort(items: list) -> list:
    for index in range(1, len(items)):
        current = items[index]
        position = index - 1

        while position >= 0 and items[position] > current:
            items[position + 1] = items[position]
            position -= 1

        items[position + 1] = current

    return items


def merge(left: list, right: list) -> list:
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(items: list) -> list:
    if len(items) <= 1:
        return items

    middle = len(items) // 2
    return merge(merge_sort(items[:middle]), merge_sort(items[middle:]))


# Simplified Timsort idea: merge sort that falls back to insertion sort on short runs
def hybrid_sort(items: list) -> list:
    if len(items) <= RUN_SIZE:
        return insertion_sort(items)

    middle = len(items) // 2
    return merge(hybrid_sort(items[:middle]), hybrid_sort(items[middle:]))


def timsort(items: list) -> list:
    return sorted(items)


def random_data(size: int) -> list:
    return [random.randint(0, size) for _ in range(size)]


def sorted_data(size: int) -> list:
    return list(range(size))


def reversed_data(size: int) -> list:
    return list(range(size, 0, -1))


def nearly_sorted_data(size: int) -> list:
    data = list(range(size))

    for _ in range(max(1, size // 20)):
        first = random.randrange(size)
        second = random.randrange(size)
        data[first], data[second] = data[second], data[first]

    return data


DATASETS = [
    ("random", random_data),
    ("sorted", sorted_data),
    ("reversed", reversed_data),
    ("nearly sorted", nearly_sorted_data),
]


def repeats_for(size: int) -> int:
    return max(1, 10_000 // size)


def measure(algorithm, data: list, repeats: int) -> float:
    timer = timeit.Timer(lambda: algorithm(list(data)))
    return timer.timeit(number=repeats) / repeats


def print_table(sizes: list, algorithms: list) -> None:
    for name, generator in DATASETS:
        header = f"{name:<15}|" + "".join(f" {title:<12}|" for title, _ in algorithms)
        print(header)
        print("-" * len(header))

        for size in sizes:
            data = generator(size)
            repeats = repeats_for(size)
            timings = [measure(algorithm, data, repeats) for _, algorithm in algorithms]
            print(f"{size:<15}|" + "".join(f" {value:<12.5f}|" for value in timings))

        print()


def print_speedup(size: int) -> None:
    data = random_data(size)
    repeats = repeats_for(size)

    merge_time = measure(merge_sort, data, repeats)
    hybrid_time = measure(hybrid_sort, data, repeats)
    timsort_time = measure(timsort, data, repeats)

    print(f"Random array of {size} elements:")
    print(f"  hybrid sort is {merge_time / hybrid_time:.2f}x faster than pure merge sort")
    print(f"  Timsort is {merge_time / timsort_time:.2f}x faster than pure merge sort")
    print(f"  Timsort is {hybrid_time / timsort_time:.2f}x faster than the hybrid sort")


def main() -> None:
    random.seed(42)
    print("Average execution time per run, seconds\n")

    print("All four algorithms")
    print_table(SIZES, [
        ("Insertion", insertion_sort),
        ("Merge", merge_sort),
        ("Hybrid", hybrid_sort),
        ("Timsort", timsort),
    ])

    print("\nLarge arrays, insertion sort excluded because of its O(n^2) growth")
    print_table(LARGE_SIZES, [
        ("Merge", merge_sort),
        ("Hybrid", hybrid_sort),
        ("Timsort", timsort),
    ])

    print()
    print_speedup(100_000)


main()
