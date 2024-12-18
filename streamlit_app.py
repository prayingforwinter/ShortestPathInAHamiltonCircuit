import streamlit as st
from streamlit_drawable_canvas import st_canvas
import networkx as nx
from hamilton_logic import find_hamiltonian_path, visualize_path
import matplotlib.pyplot as plt

# Streamlit Configuration
st.title("Hamiltonian Circuit Finder")
st.write("Add nodes by clicking on the canvas. Drag between nodes to add edges with weights.")

# Initialize Graph
if "graph" not in st.session_state:
    st.session_state.graph = nx.Graph()

graph = st.session_state.graph

# Canvas Setup
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  
    stroke_width=3,
    stroke_color="black",
    background_color="#fff",
    update_streamlit=True,
    height=500,
    width=700,
    drawing_mode="freedraw",
    key="hamilton_canvas",
)

# User Interaction Section
st.subheader("Add Node and Edges")
node_id = st.text_input("Node ID to Add:")
connect_nodes = st.text_input("Connect Nodes (comma-separated):")
edge_weight = st.number_input("Edge Weight:", min_value=1, value=1)

if st.button("Add Node"):
    graph.add_node(node_id)
    st.success(f"Added Node: {node_id}")

if st.button("Add Edge"):
    try:
        u, v = map(str.strip, connect_nodes.split(","))
        graph.add_edge(u, v, weight=edge_weight)
        st.success(f"Connected Node {u} to {v} with Weight {edge_weight}")
    except ValueError:
        st.error("Please input two nodes separated by a comma.")

# Visualize Graph
st.subheader("Graph Visualization")
if st.button("Show Graph"):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(8, 6))
    nx.draw(graph, pos, with_labels=True, node_color="lightblue", node_size=500)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    st.pyplot(plt)

# Find Hamiltonian Circuit
st.subheader("Find Hamiltonian Circuit")
start_node = st.text_input("Enter Start Node:", value="0")
if st.button("Find Circuit"):
    if start_node in graph.nodes:
        path, weight = find_hamiltonian_path(graph, start_node)
        if path:
            st.success(f"Hamiltonian Circuit Found: {path} with Weight {weight}")
            visualize_path(graph, path, "Hamiltonian Circuit")
            st.pyplot(plt)
        else:
            st.error("No Hamiltonian Circuit Found")
    else:
        st.error("Start Node does not exist in the graph.")
