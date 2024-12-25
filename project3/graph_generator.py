
import random
import networkx as nx

def generate_random_graph_nx(min_nodes, max_nodes, min_edges, max_edges, weight_range=(1, 100)):
    n_nodes = random.randint(min_nodes, max_nodes)
    max_possible_edges = n_nodes * (n_nodes - 1) // 2 
    
    n_edges = min(random.randint(min_edges, max_edges), max_possible_edges)

    if n_edges == 0 or n_nodes <= 1:
        G = nx.Graph()
        G.add_nodes_from(range(n_nodes))
        return G

    G = nx.Graph()
    G.add_nodes_from(range(n_nodes))

    all_possible_edges = [(u, v) for u in range(n_nodes) for v in range(u + 1, n_nodes)]
    random.shuffle(all_possible_edges)

    for u, v in all_possible_edges[:n_edges]:
        weight = random.randint(*weight_range)
        G.add_edge(u, v, weight=weight)

    return G