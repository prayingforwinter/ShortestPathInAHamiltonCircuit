# app.py
import streamlit as st
from hamilton import generate_graph, find_hamiltonian_path, visualize_path
import networkx as nx
import matplotlib.pyplot as plt

st.title("Hamiltonian Path Finder")

# Graph Parameters
num_nodes = st.slider("Number of Nodes", min_value=5, max_value=50, value=10)
start_node = st.number_input("Start Node", min_value=0, max_value=num_nodes - 1, value=0)

# Generate and Visualize Graph
if st.button("Generate Graph"):
    graph = generate_graph(num_nodes)
    st.write(f"Graph with {num_nodes} nodes generated.")
    fig, ax = plt.subplots()
    nx.draw(graph, with_labels=True, node_color='lightblue', node_size=500, ax=ax)
    st.pyplot(fig)

    # Find Hamiltonian Path
    best_path, min_weight = find_hamiltonian_path(graph, start_node)
    if best_path:
        st.success(f"Hamiltonian Path: {best_path} with weight {min_weight}")
        fig, ax = plt.subplots()
        visualize_path(graph, best_path, f"Best Path (Weight: {min_weight})")
        st.pyplot(fig)
    else:
        st.error("No Hamiltonian Path Found.")

if __name__ == "__main__":
    st.title("My Streamlit App")
