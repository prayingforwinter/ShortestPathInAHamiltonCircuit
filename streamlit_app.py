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
    st.subheader("Find Hamiltonian Circuit and Compare Runtime")
    start_node = st.number_input("Start Node:", min_value=0, max_value=num_nodes - 1, value=0, step=1)
    
    if st.button("Find and Compare"):
        # Hamiltonian Circuit Path
        path, weight = find_hamiltonian_path(graph, start_node)
        if path:
            st.success(f"Hamiltonian Circuit Found: {path} with Total Weight: {weight}")
            plt.figure(figsize=(10, 8))  # Larger visualization for clarity
            visualize_path(graph, path, title="Hamiltonian Circuit Path")
            st.pyplot(plt)
        else:
            st.error("No Hamiltonian Circuit Found.")
        
        # Runtime Comparison
        iterative_result, recursive_result, time_diff = compare_runtime(graph, start_node)

        st.subheader("Iterative Approach:")
        st.write(f"Path: {iterative_result[0]}")
        st.write(f"Weight: {iterative_result[1]}")
        st.write(f"Runtime: {iterative_result[2]:.4f} seconds")

        st.subheader("Recursive Approach:")
        st.write(f"Path: {recursive_result[0]}")
        st.write(f"Weight: {recursive_result[1]}")
        st.write(f"Runtime: {recursive_result[2]:.4f} seconds")

        st.subheader("Time Difference:")
        st.write(f"{time_diff:.4f} seconds")
