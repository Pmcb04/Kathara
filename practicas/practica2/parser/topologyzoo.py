import networkx as nx
import matplotlib.pyplot as plt
from functools import reduce
import xml.etree.ElementTree as ET

class TopologyZooGMLParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.graph = None
        self.nodes = []
        self.edges = []

    def parse(self):
        # Inicializa un grafo vacío
        self.graph = nx.Graph()

        with open(self.file_path, 'r') as gml_file:
            parsing_nodes = False
            parsing_edges = False
            node_data = {}
            edge_data = {}

            for line in gml_file:
                line = line.strip()

                if line == "node [":
                    parsing_nodes = True
                    node_data = {}
                elif line == "]" and parsing_nodes:
                    parsing_nodes = False
                    if node_data:
                        self.graph.add_node(node_data['id'], **node_data)
                elif parsing_nodes:
                    parts = line.split()
                    value = reduce(lambda x, y: x + ' ' + y, parts[1:]).replace('"', '')
                    node_data[parts[0]] = value

                if line == "edge [":
                    parsing_edges = True
                    edge_data = {}
                elif line == "]" and parsing_edges:
                    parsing_edges = False
                    if edge_data:
                        self.graph.add_edge(edge_data['source'], edge_data['target'], **edge_data)
                elif parsing_edges:
                    parts = line.split()
                    value = reduce(lambda x, y: x + ' ' + y, parts[1:]).replace('"', '')
                    edge_data[parts[0]] = value

        return self.graph

    def parse_nodes(self):
        if self.graph is None:
            self.parse()
        return self.graph.nodes(data=True)

    def parse_edges(self):
        if self.graph is None:
            self.parse()
        return self.graph.edges(data=True)