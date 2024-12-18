import streamlit as st
import networkx as nx
from hamilton import find_hamiltonian_path, visualize_path, add_node, add_edge

def main():
    st.title("Hamiltonian Circuit Finder")

    # Create a graph
    G = nx.Graph()
    num_nodes = st.slider("Number of Nodes", min_value=3, max_value=10, value=5)
    edges = [(i, (i + 1) % num_nodes, 1) for i in range(num_nodes)]

    for u, v, weight in edges:
        add_edge(G, u, v, weight)

    # Interactive node addition
    new_node = st.text_input("Add Node (integer):")
    connect_to = st.text_input("Connect To Node (comma-separated integers):")
    weight = st.number_input("Weight of New Edges", min_value=1, value=1)

    if st.button("Add Node and Edges"):
        try:
            new_node = int(new_node)
            connections = list(map(int, connect_to.split(",")))
            add_node(G, new_node)
            for neighbor in connections:
                add_edge(G, new_node, neighbor, weight)
            st.success(f"Added Node {new_node} and connected to {connections} with weight {weight}")
        except Exception as e:
            st.error(f"Error: {e}")

    # Start node for Hamiltonian Circuit
    start_node = st.number_input("Start Node", min_value=0, max_value=num_nodes - 1, value=0)

    if st.button("Find Hamiltonian Circuit"):
        best_path, min_weight = find_hamiltonian_path(G, start_node)
        if best_path:
            st.write(f"Hamiltonian Path: {best_path}")
            st.write(f"Minimum Weight: {min_weight}")
            visualize_path(G, best_path, "Hamiltonian Circuit")
        else:
            st.write("No Hamiltonian Path Found")

if __name__ == "__main__":
    main()
