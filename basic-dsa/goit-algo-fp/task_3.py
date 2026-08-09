import heapq

GRAPH = {
    "A": {"B": 7, "C": 9, "F": 14},
    "B": {"A": 7, "C": 10, "D": 15},
    "C": {"A": 9, "B": 10, "D": 11, "F": 2},
    "D": {"B": 15, "C": 11, "E": 6},
    "E": {"D": 6, "F": 9, "G": 4},
    "F": {"A": 14, "C": 2, "E": 9},
    "G": {"E": 4},
}


def dijkstra(graph: dict, start: str) -> tuple:
    distances = {vertex: float("inf") for vertex in graph}
    previous = {vertex: None for vertex in graph}
    distances[start] = 0

    visited = set()
    heap = [(0, start)]

    while heap:
        current_distance, current = heapq.heappop(heap)

        if current in visited:
            continue

        visited.add(current)

        for neighbour, weight in graph[current].items():
            distance = current_distance + weight

            if distance < distances[neighbour]:
                distances[neighbour] = distance
                previous[neighbour] = current
                heapq.heappush(heap, (distance, neighbour))

    return distances, previous


def build_path(previous: dict, target: str) -> list:
    path = []

    while target is not None:
        path.append(target)
        target = previous[target]

    path.reverse()
    return path


def report(graph: dict, start: str) -> None:
    distances, previous = dijkstra(graph, start)

    print(f"Shortest paths from vertex {start}")
    header = f"{'Vertex':<8}| {'Distance':<10}| Path"
    print(header)
    print("-" * (len(header) + 12))

    for vertex in sorted(graph):
        distance = distances[vertex]

        if distance == float("inf"):
            print(f"{vertex:<8}| {'unreachable':<10}| -")
            continue

        path = " -> ".join(build_path(previous, vertex))
        print(f"{vertex:<8}| {distance:<10}| {path}")

    print()


def main() -> None:
    edges = sum(len(neighbours) for neighbours in GRAPH.values()) // 2
    print(f"Graph: {len(GRAPH)} vertices, {edges} edges\n")

    for vertex in sorted(GRAPH):
        neighbours = ", ".join(f"{name}({weight})" for name, weight in GRAPH[vertex].items())
        print(f"  {vertex}: {neighbours}")

    print()
    report(GRAPH, "A")
    report(GRAPH, "D")


main()
