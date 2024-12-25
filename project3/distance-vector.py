import graph_generator
import dijkstra
import random
import time
from tqdm import tqdm
import networkx as nx

def distance_vector(graph):
    routing_table = {node: {neighbor: edge_info['weight'] for neighbor, edge_info in graph[node].items()} for node in graph}
    
    for _ in range(len(graph)):
        for node in graph:
            for neighbor in graph[node]:
                for next_node in graph:
                    if next_node not in routing_table[node]:
                        routing_table[node][next_node] = float('inf')
                    if next_node in graph[neighbor] and routing_table[node][next_node] > routing_table[node][neighbor] + routing_table[neighbor][next_node]:
                        routing_table[node][next_node] = routing_table[node][neighbor] + routing_table[neighbor][next_node]
    
    return routing_table

def UnitTest_distance_vector(num_tests, min_nodes=5, max_nodes=15, min_edges=5, max_edges=25, weight_range=(1, 50), is_required_pathMatch=False, use_time_as_seed = False):
    max_iterations = 1000
    if use_time_as_seed:
        random.seed(int(time.time()))
    else:
        random.seed(42) 

    path_unMatchTime = 0

    pbar = tqdm(total=num_tests, desc="Running tests")
    for test_id in range(1, num_tests + 1):
        graph = graph_generator.generate_random_graph_nx(min_nodes, max_nodes, min_edges, max_edges, weight_range)
        start_node = random.randint(0, len(graph.nodes) - 1)

        nx_distances, nx_paths = nx.single_source_dijkstra(graph, start_node)

        graph_dict = {node: dict(graph[node]) for node in graph}
        my_distances, my_paths = dijkstra.dijkstra(graph_dict, start_node)

        my_distances_filtered = {k: v for k, v in my_distances.items() if v < float('inf')}
        my_paths_filtered = {k: v for k, v in my_paths.items() if v}

        dv_routing_table = distance_vector(graph_dict)
        dv_distances = {}
        for node in graph:
            dv_distances[node] = dv_routing_table[start_node].get(node, float('inf'))
        dv_paths = {node: [start_node] for node in dv_routing_table}
        for node in dv_routing_table:
            iterations = 0
            while dv_paths[node][-1] != node and iterations < max_iterations:
                current = dv_paths[node][-1]
                if current not in dv_routing_table or not dv_routing_table[current]:
                    break
                next_hop = min(dv_routing_table[current], key=dv_routing_table[current].get)
                if next_hop in dv_paths[node]:
                    break
                dv_paths[node].append(next_hop)
                iterations += 1

        if is_required_pathMatch:
            for node in graph:
                if nx_paths[node] != dv_paths[node]:
                    path_unMatchTime += 1
                    break

        pbar.update(1)
    pbar.close()

    print("\nAll tests passed successfully! 🎉")

    return path_unMatchTime


if __name__ == "__main__":
    n = int(input("Enter the test times: "))
    
    n = UnitTest_distance_vector(num_tests = n, is_required_pathMatch = False, use_time_as_seed = True)

    print(f"Path unmatch times: {n}")