import os

from pyvis.network import Network
import networkx as nx

from content_manager import ContentManager
from triples_extraction import extract_triples
from triples_standardization import standardize_triples
from utils import write_to_file, read_from_file


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


def create_knowledge_graph(content_manager: ContentManager):

    kg_triples_path = os.path.abspath('./data/knowledge_graph.txt')
    kg_graph_path = os.path.abspath('./data/knowledge_graph.html')

    # get the twice merged narratives (with iteration max_iterations + 1 = 4)
    narratives = [n for n in content_manager.narratives.values() if n.iteration == 4]

    # collect all triples
    all_triples = set()
    for narrative in narratives:
        triples = extract_triples(narrative.description)
        all_triples.update(triples)

    # standardize triples
    sorted_triples = sorted(all_triples, key=lambda x: ''.join(x))
    standardized_triples = standardize_triples(sorted_triples)

    # same triples as text file
    write_to_file(kg_triples_path, str(sorted(standardized_triples, key=lambda x: ''.join(x))))
    # visualize graph in HTML
    visualize_knowledge_graph(list(standardized_triples), kg_graph_path)

    return kg_triples_path, kg_graph_path


def main(content_file_path: str):
    try:
        if os.path.exists(content_file_path):
            content_manager = ContentManager()
            content_json = read_from_file(content_file_path)
            content_manager.deserialize(content_json)
            kg_triples_path, kg_graph_path = create_knowledge_graph(content_manager)
            print(f"Knowledge graph created:\n{kg_triples_path}\n{kg_graph_path}")
        else:
            print(f"File not found: {content_file_path}")
    except Exception as e:
        print(f"Exception while creating a knowledge graph: {e}")


if __name__ == '__main__':
    main('./data/content.json')
