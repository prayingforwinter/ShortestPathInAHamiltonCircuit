import networkx as nx
import itertools
import matplotlib.pyplot as plt
import time

def find_hamiltonian_path(graph, start_node):
    nodes = list(graph.nodes)
    nodes.remove(start_node)
    
    min_weight = float('inf')
    best_path = None

    for perm in itertools.permutations(nodes):
        path = [start_node] + list(perm) + [start_node]
        try:
            weight = sum(graph[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))
        except KeyError:
            continue  # Skip paths with missing edges

        if weight < min_weight:
            min_weight = weight
            best_path = path

    return best_path, min_weight

def visualize_path(graph, path, title):
    pos = nx.spring_layout(graph, seed=42)
    plt.figure(figsize=(8, 6))
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)

    # Highlight the path
    if path:
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=2.5)

    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.title(title)
    plt.show()
