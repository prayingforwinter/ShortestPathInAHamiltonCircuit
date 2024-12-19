import itertools
import networkx as nx
import matplotlib.pyplot as plt
import time

def find_hamiltonian_path_iterative(graph, start_node):
    """Finds the Hamiltonian Circuit using an iterative approach."""
    nodes = list(graph.nodes)
    nodes.remove(start_node)
    
    min_weight = float('inf')
    best_path = None

    start_time = time.time()  # Start timing
    for perm in itertools.permutations(nodes):
        path = [start_node] + list(perm) + [start_node]
        try:
            weight = sum(graph[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))
        except KeyError:
            continue  # Skip paths with missing edges

        if weight < min_weight:
            min_weight = weight
            best_path = path
    end_time = time.time()  # End timing

    runtime = end_time - start_time
    return best_path, min_weight, runtime


def find_hamiltonian_path_recursive(graph, start_node):
    """Finds the Hamiltonian Circuit using a recursive approach."""
    nodes = list(graph.nodes)
    nodes.remove(start_node)

    def helper(path, remaining_nodes):
        if not remaining_nodes:
            # Check if there's an edge back to the start node
            if graph.has_edge(path[-1], path[0]):
                path.append(path[0])  # Form the circuit
                weight = sum(graph[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))
                return path, weight
            return None, float('inf')

        min_path, min_weight = None, float('inf')
        for next_node in remaining_nodes:
            new_path = path + [next_node]
            sub_path, sub_weight = helper(new_path, [n for n in remaining_nodes if n != next_node])
            if sub_weight < min_weight:
                min_path, min_weight = sub_path, sub_weight

        return min_path, min_weight

    start_time = time.time()  # Start timing
    best_path, min_weight = helper([start_node], nodes)
    end_time = time.time()  # End timing

    runtime = end_time - start_time
    return best_path, min_weight, runtime


def visualize_path(graph, path, title):
    """Visualizes the graph with the Hamiltonian Circuit highlighted."""
    pos = nx.spring_layout(graph, seed=42)
    plt.figure(figsize=(8, 6))

    # Draw the full graph
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)

    # Highlight the Hamiltonian Circuit path
    if path:
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=2.5)

    # Display weights
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    plt.title(title)
    plt.show()


def compare_runtime(graph, start_node):
    """Compares the runtime of iterative and recursive Hamiltonian pathfinding approaches."""
    # Iterative approach
    iterative_path, iterative_weight, iterative_time = find_hamiltonian_path_iterative(graph, start_node)

    # Recursive approach
    recursive_path, recursive_weight, recursive_time = find_hamiltonian_path_recursive(graph, start_node)

    # Print results
    print("Iterative Approach:")
    print(f"Path: {iterative_path}")
    print(f"Weight: {iterative_weight}")
    print(f"Runtime: {iterative_time:.4f} seconds\n")

    print("Recursive Approach:")
    print(f"Path: {recursive_path}")
    print(f"Weight: {recursive_weight}")
    print(f"Runtime: {recursive_time:.4f} seconds\n")

    time_difference = abs(iterative_time - recursive_time)
    print(f"Time Difference (Iterative - Recursive): {time_difference:.4f} seconds")

    return (iterative_path, iterative_weight, iterative_time), (recursive_path, recursive_weight, recursive_time), time_difference
