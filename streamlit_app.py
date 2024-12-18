import streamlit as st
import networkx as nx
import random
import matplotlib.pyplot as plt
from hamilton import find_hamiltonian_path, visualize_path

# Streamlit UI
st.title("Hamiltonian Circuit Finder")
st.write("Generate a random graph and find the Hamiltonian Circuit.")

# Slider for Number of Nodes
num_nodes = st.slider("Select Number of Nodes:", min_value=3, max_value=20, value=5)

# Generate Random Graph Button
if st.button("Generate Random Graph"):
    # Initialize the graph
    st.session_state.graph = nx.complete_graph(num_nodes)  # Ensures a connected graph

    # Add random weights to edges
    for u, v in st.session_state.graph.edges():
        weight = random.randint(1, 20)
        st.session_state.graph[u][v]['weight'] = weight

    st.success(f"Generated a graph with {num_nodes} nodes and random edge weights!")

# Display Graph
if "graph" in st.session_state:
    graph = st.session_state.graph

    st.subheader("Generated Graph:")
    pos = nx.spring_layout(graph, seed=42)  # Layout for consistent positioning
    plt.figure(figsize=(8, 6))
    nx.draw(graph, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10)

    # Display edge weights
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    st.pyplot(plt)

    # Hamiltonian Circuit Finder
    st.subheader("Find Hamiltonian Circuit")
    start_node = st.number_input("Select Start Node:", min_value=0, max_value=num_nodes-1, value=0, step=1)
    
    if st.button("Find Hamiltonian Circuit"):
        path, weight = find_hamiltonian_path(graph, start_node)
        if path:
            st.success(f"Hamiltonian Circuit: {path} with Minimum Weight: {weight}")
            visualize_path(graph, path, "Hamiltonian Circuit")
            st.pyplot(plt)
        else:
            st.error("No Hamiltonian Circuit Found!")
