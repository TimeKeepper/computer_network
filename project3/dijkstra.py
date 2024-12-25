# Assignment 3.1: Dijkstra algorithm. 
# In this assignment, you will develop a Dijkstra algorithm in Python. You should write python script to develop it. 
# For the program: 
# Input a topology of network nodes and a specified node.
# Output the distance list and path from the specified node to other nodes. 
# Be able to compute distance and path of any node in topology. 

import networkx as nx
import random
import heapq
from tqdm import tqdm
import time
import graph_generator

def dijkstra(graph, start_node):
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    priority_queue = [(0, start_node)]
    paths = {node: [] for node in graph}
    paths[start_node] = [start_node]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue

        for neighbor, edge_info in graph[current_node].items():
            weight = edge_info['weight']
            new_distance = distances[current_node] + weight
            
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                paths[neighbor] = paths[current_node] + [neighbor]
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return distances, paths


def UnitTest_dijkstra(num_tests, min_nodes=5, max_nodes=15, min_edges=5, max_edges=25, weight_range=(1, 50), is_required_pathMatch=False, use_time_as_seed = False):
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
        my_distances, my_paths = dijkstra(graph_dict, start_node)

        my_distances_filtered = {k: v for k, v in my_distances.items() if v < float('inf')}
        my_paths_filtered = {k: v for k, v in my_paths.items() if v}

        try:
            assert my_distances_filtered == nx_distances, "Distances do not match!"
            if (my_paths_filtered != nx_paths):
                assert is_required_pathMatch == False, "Paths do not match!"
                path_unMatchTime += 1
            pbar.update(1)
            if test_id == num_tests:
                pbar.close()

        except AssertionError as e:
            print(f"Test {test_id} failed! ❌")
            print(str(e))
            print(f"Graph: {dict(graph_dict)}")
            print(f"Start Node: {start_node}")
            print(f"Expected Distances: \t{dict(sorted(nx_distances.items()))}")
            print(f"Your Distances: \t{dict(sorted(my_distances_filtered.items()))}")
            print(f"Expected Paths: \t{dict(sorted(nx_paths.items()))}")
            print(f"Your Paths: \t\t{dict(sorted(my_paths_filtered.items()))}")
            continue
    print("\nAll tests passed successfully! 🎉")

    return path_unMatchTime

if __name__ == "__main__":
    n = int(input("Enter the test times: "))

    n = UnitTest_dijkstra(num_tests = n, is_required_pathMatch = False, use_time_as_seed = True)

    print(f"Path unmatch times: {n}")
