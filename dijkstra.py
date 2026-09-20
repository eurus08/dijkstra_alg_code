from heapq import heappush, heappop


def dijkstra(graph, source, destination, blocked=None):
    """Shortest path from source to destination as a list of nodes.

    graph is {node: {neighbour: weight}}. blocked is an optional set of nodes
    that may not be used (the dynamic model's set V). Returns None when the
    destination cannot be reached.
    """
    blocked = {str(n) for n in (blocked or ())}
    if source in blocked or destination in blocked:
        return None

    label = {source: 0}
    previous = {}
    visited = set()
    min_heap = [(0, source)]

    while min_heap:
        dist, node = heappop(min_heap)
        if node in visited:
            continue
        visited.add(node)
        if node == destination:
            break
        for neighbour, weight in graph[node].items():
            if neighbour in visited or neighbour in blocked:
                continue
            new_label = dist + weight
            if new_label < label.get(neighbour, float('inf')):
                label[neighbour] = new_label
                previous[neighbour] = node
                heappush(min_heap, (new_label, neighbour))

    if destination not in visited:
        return None

    path = [destination]
    while path[-1] != source:
        path.append(previous[path[-1]])
    return path[::-1]


def path_length(graph, path):
    return round(sum(graph[a][b] for a, b in zip(path, path[1:])), 2)
