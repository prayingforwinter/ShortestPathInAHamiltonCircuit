import streamlit as st
import networkx as nx
import random
import matplotlib.pyplot as plt
import math
import time
from hamilton import (
    find_hamiltonian_path_iterative,
    find_hamiltonian_path_recursive,
    visualize_path,
)

# Streamlit UI
st.title("Hamiltonian Circuit Finder")
st.write("Generate a random graph and find the Hamiltonian Circuit using both iterative and recursive approaches.")

# Slider for Number of Nodes
num_nodes = st.slider("Select Number of Nodes:", min_value=3, max_value=15, value=5)

# Generate Random Graph Button
if st.button("Generate Random Graph"):
    # Initialize the graph
    st.session_state.graph = nx.complete_graph(num_nodes)  # Ensures a connected graph

    # Add random weights to edges
    for u, v in st.session_state.graph.edges():
        weight = random.randint(1, 20)
        st.session_state.graph[u][v]['weight'] = weight

    # Calculate expected runtime
    expected_runtime = math.factorial(num_nodes)  # O(n!)
    st.session_state.expected_runtime = expected_runtime
    st.success(f"Generated a graph with {num_nodes} nodes and random edge weights!")
    st.info(f"Expected Time Complexity: O({num_nodes}!) ≈ {expected_runtime} permutations to check.")

# Display Graph
if "graph" in st.session_state:
    graph = st.session_state.graph

    st.subheader("Generated Graph:")
    pos = nx.spring_layout(graph, seed=42)  # Layout for consistent positioning
    plt.figure(figsize=(10, 8))  # Larger visualization
    nx.draw(graph, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10)

    # Display edge weights
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    st.pyplot(plt)

    # Input for Start Node
    st.subheader("Find Hamiltonian Circuit")
    start_node = st.number_input("Start Node:", min_value=0, max_value=num_nodes - 1, value=0, step=1)

    # Single Button for Combined Functionality
    if st.button("Find Hamiltonian Circuit and Compare Runtime"):
        # Start runtime counter
        start_time = time.time()


        # Iterative approach
        iterative_result = find_hamiltonian_path_iterative(graph, start_node)
        iterative_path, iterative_weight, iterative_runtime = iterative_result

        # Visualize the iterative path (or choose one to display)
        if iterative_path:
            plt.figure(figsize=(10, 8))  # Larger visualization for clarity
            visualize_path(graph, iterative_path, title="Result using Iterative")
            st.pyplot(plt)

             # Display the results
        st.subheader("Iterative Approach:")
        st.write(f"Path: {iterative_path}")
        st.write(f"Weight: {iterative_weight}")
        st.write(f"Runtime: {iterative_runtime:.4f} seconds")

        # Recursive approach
        recursive_result = find_hamiltonian_path_recursive(graph, start_node)
        recursive_path, recursive_weight, recursive_runtime = recursive_result

        if recursive_path:
            plt.figure(figsize=(10, 8))  # Larger visualization for clarity
            visualize_path(graph, recursive_path, title="Result using Recursive")
            st.pyplot(plt)


        st.subheader("Recursive Approach:")
        st.write(f"Path: {recursive_path}")
        st.write(f"Weight: {recursive_weight}")
        st.write(f"Runtime: {recursive_runtime:.4f} seconds")

        st.subheader("Time Difference:")
        time_diff = abs(iterative_runtime - recursive_runtime)
        st.write(f"{time_diff:.4f} seconds")
