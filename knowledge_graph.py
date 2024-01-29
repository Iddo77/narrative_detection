from pyvis.network import Network
import networkx as nx


def visualize_knowledge_graph(triples, output_path):
    # Create a NetworkX graph
    G = nx.Graph()
    for node1, edge, node2 in triples:
        G.add_node(node1)
        G.add_node(node2)
        G.add_edge(node1, node2, title=edge)

    # Initialize PyVis network without assuming Jupyter Notebook
    net = Network(notebook=False, height="750px", width="100%")
    net.from_nx(G)

    # Save the graph to the specified directory
    net.save_graph(output_path)
