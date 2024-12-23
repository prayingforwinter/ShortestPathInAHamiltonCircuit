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


import time

def find_hamiltonian_path_recursive(graph, start_node):
    """Finds the Hamiltonian Circuit using a tail-recursive approach."""
    import time  # Ensure timing is properly accounted for

    nodes = list(graph.nodes)
    nodes.remove(start_node)

    def tail_recursive_helper(path, remaining_nodes, min_path, min_weight):
        # Base case: all nodes visited
        if not remaining_nodes:
            if graph.has_edge(path[-1], start_node):
                path.append(start_node)  # Form the circuit
                weight = sum(graph[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))
                if weight < min_weight:
                    return path, weight
            return min_path, min_weight

        # Recursively process each node in remaining_nodes
        def explore_next(index, current_min_path, current_min_weight):
            if index == len(remaining_nodes):  # Base case for recursion
                return current_min_path, current_min_weight
            
            next_node = remaining_nodes[index]
            new_path = path + [next_node]
            rest_nodes = remaining_nodes[:index] + remaining_nodes[index + 1:]

            # Explore with the current node
            updated_path, updated_weight = tail_recursive_helper(new_path, rest_nodes, current_min_path, current_min_weight)

            # Continue exploring the remaining nodes
            return explore_next(index + 1, updated_path, updated_weight)

        # Start the recursive exploration
        return explore_next(0, min_path, min_weight)

    start_time = time.perf_counter()  # Start timing with high resolution
    best_path, min_weight = tail_recursive_helper([start_node], nodes, None, float('inf'))
    end_time = time.perf_counter()  # End timing with high resolution

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

def compare_execution_times_live(graph, start_node):
    """Compares and plots execution times for iterative and recursive Hamiltonian path searches in real-time."""
    iterative_times = []
    recursive_times = []
    node_counts = range(4, len(graph.nodes) + 1)  # Use a subset of nodes for timing comparison

    for n in node_counts:
        # Generate a complete graph with `n` nodes
        subgraph = nx.complete_graph(n)
        for u, v in subgraph.edges:
            subgraph[u][v]['weight'] = (u + v + 1)  # Assign random weights for simplicity

        # Measure iterative execution time
        start_time = time.time()
        _ = find_hamiltonian_path_iterative(subgraph, start_node)
        end_time = time.time()
        iterative_times.append(end_time - start_time)

        # Measure recursive execution time
        start_time = time.time()
        _ = find_hamiltonian_path_recursive(subgraph, start_node)
        end_time = time.time()
        recursive_times.append(end_time - start_time)

        # Update plot in real-time
        plt.clf()  # Clear previous plot
        plt.plot(node_counts[:len(iterative_times)], iterative_times, 'r-o', label="Iterative")
        plt.plot(node_counts[:len(recursive_times)], recursive_times, 'b-o', label="Recursive")
        plt.title("Real-Time Hamiltonian Path Execution Time Comparison")
        plt.xlabel("Number of Nodes (n)")
        plt.ylabel("Execution Time (seconds)")
        plt.legend()
        plt.grid(True)
        plt.pause(0.5)  # Pause to show updates

    plt.show()

    return iterative_times, recursive_times, node_counts
