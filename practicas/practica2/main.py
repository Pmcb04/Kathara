import sys
from parser.topologyzoo import TopologyZooGraphMLParser
from parser.topologyzoo import TopologyZooGMLParser
from parser.sndlib import SNDLibXMLParser

def parse_command_line_args(args):
    if len(args) != 4:
        print("Use: python main.py <dataset> <format> <path_file>")
        print()
        print("Argumentos validos:")
        print("Dataset -> [topologyzoo]")
        print("Format -> [gml graphml]")
        sys.exit(1)

    dataset = args[1]
    file_format = args[2]
    file_path = args[3]

    if dataset == "topologyzoo":
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
        print("Conjunto de datos no válido. Use 'topologyzoo'.")
        sys.exit(1)


    return nodes, edges

if __name__ == "__main__":
    nodes, edges = parse_command_line_args(sys.argv)
    
    # Accede a los nodos
    print("\nNodos:")
    for node in nodes:
        print(nodes)

    # Accede a las aristas (edges)
    print("\nAristas (Edges):")
    for edge in edges:
        print(edge)

    # Importar la biblioteca de Kathara
    from kathara import Kathara

    # Crear una instancia de la topología de Kathara
    topo = Kathara()

    # Agregar nodos a la topología
    nodo1 = topo.createNode("nodo1")
    nodo2 = topo.createNode("nodo2")
    nodo3 = topo.createNode("nodo3")

    # Conectar nodos entre sí
    topo.createLink(nodo1, nodo2)
    topo.createLink(nodo2, nodo3)

    # Configurar las interfaces de red en los nodos
    nodo1.createInterface(name="eth0", ip="192.168.1.1/24")
    nodo2.createInterface(name="eth0", ip="192.168.1.2/24")
    nodo2.createInterface(name="eth1", ip="192.168.2.1/24")
    nodo3.createInterface(name="eth0", ip="192.168.2.2/24")

    # Iniciar la topología
    topo.start()
