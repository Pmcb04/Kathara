import networkx as nx
import matplotlib.pyplot as plt
from functools import reduce
import xml.etree.ElementTree as ET

class TopologyZooGMLParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.graph = None

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
                elif line == "]":
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
                elif line == "]":
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


class TopologyZooGraphMLParser:
    def __init__(self, filename):
        self.filename = filename
        self.graph_data = None
        self.nodes = []
        self.edges = []
        self.key_to_name = {}
        self.graphml_namespace = "{http://graphml.graphdrawing.org/xmlns}"
        self.parse()

    def parse(self):
        try:
            tree = ET.parse(self.filename)
            root = tree.getroot()

            # Extraer las definiciones de clave
            self.parse_keys(root)

            # Buscar el elemento 'graph' en el archivo
            graph = root.find(f"{self.graphml_namespace}graph")
            
            if graph is not None:
                self.graph_data = self.parse_graph_data(graph)
                self.nodes = self.parse_nodes(graph)
                self.edges = self.parse_edges(graph)
            else:
                raise Exception("No se encontró el elemento 'graph' en el archivo XML.")

        except ET.ParseError as e:
            raise Exception(f"Error al analizar el archivo XML: {str(e)}")

    def parse_keys(self, root):
        key_elements = root.findall(f".//{self.graphml_namespace}key")
        for key_element in key_elements:
            key_id = key_element.get("id")
            key_name = key_element.get("attr.name")
            self.key_to_name[key_id] = key_name

    def parse_graph_data(self, graph):
        data = {}
        for data_element in graph.findall(f"{self.graphml_namespace}data"):
            key = data_element.get("key")
            value = data_element.text
            name = self.key_to_name.get(key, key)
            data[name] = value
        return data

    def parse_nodes(self, graph):
        nodes = []
        for node_element in graph.findall(f"{self.graphml_namespace}node"):
            node_id = node_element.get("id")
            node_data = self.parse_node_data(node_element)
            nodes.append({"id": node_id, "data": node_data})
        return nodes

    def parse_node_data(self, node_element):
        data = {}
        for data_element in node_element.findall(f"{self.graphml_namespace}data"):
            key = data_element.get("key")
            value = data_element.text
            name = self.key_to_name.get(key, key)
            data[name] = value
        return data

    def parse_edges(self, graph):
        edges = []
        for edge_element in graph.findall(f"{self.graphml_namespace}edge"):
            source = edge_element.get("source")
            target = edge_element.get("target")
            edge_data = self.parse_edge_data(edge_element)
            edges.append({"source": source, "target": target, "data": edge_data})
        return edges

    def parse_edge_data(self, edge_element):
        data = {}
        for data_element in edge_element.findall(f"{self.graphml_namespace}data"):
            key = data_element.get("key")
            value = data_element.text
            name = self.key_to_name.get(key, key)
            data[name] = value
        return data