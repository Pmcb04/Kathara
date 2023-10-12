import sys
from parser.topologyzoo import TopologyZooGraphMLParser
from parser.topologyzoo import TopologyZooGMLParser

def parse_command_line_args(args):
    if len(args) != 4:
        print("Use: python main.py <dataset> <format> <path_file>")
        print()
        print("Argumentos validos:")
        print("Dataset -> [sndlib topologyzoo]")
        print("Format -> sndlib[native xml] topologyzoo[gml graphml]")
        sys.exit(1)

    dataset = args[1]
    file_format = args[2]
    file_path = args[3]

    if dataset == "sndlib":
        if file_format == "native":
            print(f"Procesando SNDLib dataset en formato {file_format} desde {file_path}.")
        elif file_format == "xml":
            print(f"Procesando SNDLib dataset en formato {file_format} desde {file_path}.")
        else:
            print("Formato no válido para SNDLib. Use 'native' o 'xml'.")
            sys.exit(1)
    elif dataset == "topologyzoo":
        if file_format == "gml":
            print(f"Procesando TopologyZoo dataset en formato {file_format} desde {file_path}.")
            parser = TopologyZooGMLParser(file_path)
            nodes = parser.parse_nodes()
            edges = parser.parse_edges()
        elif file_format == "graphml":
            print(f"Procesando TopologyZoo dataset en formato {file_format} desde {file_path}.")
            parser = TopologyZooGraphMLParser(file_path)
            nodes = parser.nodes
            edges = parser.edges
        else:
            print("Formato no válido para TopologyZoo. Use 'gml' o 'graphml'.")
            sys.exit(1)
    else:
        print("Conjunto de datos no válido. Use 'sndlib' o 'topologyzoo'.")
        sys.exit(1)


    return nodes, edges



if __name__ == "__main__":
    nodes, edges = parse_command_line_args(sys.argv)
  

    # Accede a los nodos
    print("\nNodos:")
    for node in nodes:
        nodes[node.id] = Node()

    # Accede a las aristas (edges)
    print("\nAristas (Edges):")
    for edge in edges:
        print(edge)
    routers, network = nodes_edges_to_kathara(nodes, edges)

    # TODO convert nodes and edge to kathara

    