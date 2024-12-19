import streamlit as st
import networkx as nx
import random
import matplotlib.pyplot as plt
from hamilton import find_hamiltonian_path_iterative, find_hamiltonian_path_recursive, visualize_path, compare_runtime

# Streamlit UI
st.title("Hamiltonian Circuit Finder")
st.write("Generate a random graph, find the Hamiltonian Circuit, and compare performance.")

# Slider for Number of Nodes
num_nodes = st.slider("Select Number of Nodes:", min_value=3, max_value=20, value=5)

# Button to generate random graph
if st.button("Generate Random Graph"):
    # Generate a connected graph
    graph = nx.complete_graph(num_nodes)
    for u, v in graph.edges():
        graph[u][v]['weight'] = random.randint(1, 20)
    st.session_state.graph = graph
    st.success(f"Random graph with {num_nodes} nodes generated.")

# Display the generated graph
if "graph" in st.session_state:
    st.subheader("Generated Graph:")
    graph = st.session_state.graph
    pos = nx.spring_layout(graph, seed=42)
    
    plt.figure(figsize=(10, 8))  # Adjusted size for better visibility
    nx.draw(graph, pos, with_labels=True, node_color="lightblue", node_size=700, font_size=12)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    st.pyplot(plt)

    # Find Hamiltonian Circuit and Compare Runtime
    if st.button("Find Hamiltonian Circuit and Compare Runtime"):
    # Iterative approach
    iterative_result = find_hamiltonian_path_iterative(graph, start_node)
    iterative_path, iterative_weight, iterative_runtime = iterative_result

    # Recursive approach
    recursive_result = find_hamiltonian_path_recursive(graph, start_node)
    recursive_path, recursive_weight, recursive_runtime = recursive_result

    # Visualize the iterative path (or choose one to display)
    if iterative_path:
        plt.figure(figsize=(10, 8))  # Larger visualization for clarity
        visualize_path(graph, iterative_path, title="Hamiltonian Circuit Path (Iterative)")
        st.pyplot(plt)

    # Display the results
    st.subheader("Iterative Approach:")
    st.write(f"Path: {iterative_path}")
    st.write(f"Weight: {iterative_weight}")
    st.write(f"Runtime: {iterative_runtime:.4f} seconds")

    st.subheader("Recursive Approach:")
    st.write(f"Path: {recursive_path}")
    st.write(f"Weight: {recursive_weight}")
    st.write(f"Runtime: {recursive_runtime:.4f} seconds")

    st.subheader("Time Difference:")
    st.write(f"{abs(iterative_runtime - recursive_runtime):.4f} seconds")
