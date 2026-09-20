from heapq import heappush, heappop


def dikjstra(graph,source,destination):

    inf = float('inf')

    node_data = {}
    for node in graph:
        temp_dict = {"label":inf, "path": []}
        node_data[node] = temp_dict

    node_data[source]["label"] = 0

    temporary = []
    min_heap = []
    current_node = source

    while current_node != destination:
        if current_node not in temporary:
            temporary.append(current_node)
            for connected_node in graph[current_node]:
                if connected_node not in temporary:
                    new_label = node_data[current_node]["label"] + graph[current_node][connected_node]
                    if new_label < node_data[connected_node]["label"]:
                        node_data[connected_node]["label"]  = new_label
                        node_data[connected_node]["path"] = node_data[current_node]["path"].copy()
                        node_data[connected_node]["path"].append(current_node)
                    heappush(min_heap, (node_data[connected_node]["label"], connected_node))


        current_path, current_node = heappop(min_heap)

    node_data[destination]['path'].append(destination)
    return node_data[destination]['path']#, round(node_data[destination]['label'], 3)


