import os
import sys
import math
import hashlib
import shutil
from parser.topologyzoo import TopologyZooGMLParser
from classes.subnet_generator import SubnetGenerator

network_gen_mask = 30
network_gen = "10.0.0.0"
change_text = '[change]'
network_text = '[network]'
file_rip = 'etc/quagga/ripd.conf'
file_ospfd = 'etc/quagga/ospfd.conf'

def parse_command_line_args(args):
    if len(args) != 5:
        print("Use: python main.py <dataset> <format> <routing> <path_file>")
        print()
        print("Argumentos validos:")
        print("Dataset -> [topologyzoo]")
        print("Format -> [gml]")
        print("Routing -> [rip opsf]")
        sys.exit(1)

    dataset = args[1]
    file_format = args[2]
    routing = args[3]
    file_path = args[4]

    if dataset == "topologyzoo":
        if file_format == "gml":
            print(f"Procesando TopologyZoo dataset en formato {file_format} desde {file_path}.")
            parser = TopologyZooGMLParser(file_path)
            nodes = parser.parse_nodes()
            edges = parser.parse_edges()
        else:
            print("Formato no válido para TopologyZoo. Use 'gml'.")
            sys.exit(1)

        if routing != "rip" and routing != "ospf" :
            print("Formato no válido para Routing. Use 'rip' o 'ospf'.")
            sys.exit(1)
    else:
        print("Conjunto de datos no válido. Use 'topologyzoo'.")
        sys.exit(1)

    lab_name = file_route(file_path)

    return nodes, edges, routing, lab_name

def haversine_distance(lat1, lon1, lat2, lon2):
    # Radio de la Tierra en kilómetros
    radius = 6371.0

    # Convertir las coordenadas de grados a radianes
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Diferencia de latitud y longitud
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula de Haversine
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distancia en kilómetros
    distance = radius * c
    return distance

def file_route(route):
    file = os.path.basename(route) # file name
    file, _ = os.path.splitext(file) # file name without extension
    return file

def create_folder(folder):
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
            print(f'Se ha creado la carpeta: {folder}')
        except OSError as e:
            print(f'Error al crear la carpeta: {e}')

def copy_folder(source, target):
    try:
        if os.path.exists(target):
            shutil.rmtree(target)

        shutil.copytree(source, target)
    except Exception as e:
        print(f'Error al copiar: {e}')

def create_test_machine(path_test_file, interfaces, id_machine):
    with open(path_test_file, 'w') as test:
        for interfaces_machine in interfaces:
            for interface in range(0, len(interfaces_machine)):
                if interface != id_machine:
                    test.write(f"route\n")
                    test.write(f'echo "-------------------------------------------"\n')
                    test.write(f"ping -c 1 {interfaces_machine[interface]['ip_address']}\n")
                    test.write(f'echo "-------------------------------------------"\n')
                    test.write(f"traceroute {interfaces_machine[interface]['ip_address']}\n")
                    test.write(f'echo "-------------------------------------------"\n\n')

if __name__ == "__main__":
    nodes, edges, routing, lab_name = parse_command_line_args(sys.argv)
    path_lab = "generate/" + lab_name
    path_test = path_lab + '/_test'
    create_folder(path_lab)
    create_folder(path_test)
    routers = list(nodes)
    networks = list(edges)

    interfaces = [[] for _ in routers]

    subnet_gen = SubnetGenerator(network_gen, network_gen_mask)

    topology = open(path_lab + '/' + lab_name + '_topology.txt', 'w')
    title_network = "------------------------------------ Networks\n"
    print(title_network)
    topology.write(title_network)
    for network in networks:
        subnet = subnet_gen.get_next_subnet()
        network[2]['network'] = subnet
        network[2]['label'] = hashlib.sha256(str(network[2]).encode()).hexdigest() # hash para el nombre de la red
        router_source = routers[int(network[0])]
        router_target = routers[int(network[1])]
        weight_interface = haversine_distance(
            float(router_source[1]['Latitude']), 
            float(router_source[1]['Longitude']), 
            float(router_target[1]['Latitude']),
            float(router_target[1]['Longitude']))
        interfaces[int(network[0])].append({
            'label': network[2]['label'], 
            'ip_address': str(network[2]['network'].network_address + 1), 
            'weight' : weight_interface
        })
        interfaces[int(network[1])].append({
            'label': network[2]['label'], 
            'ip_address': str(network[2]['network'].network_address + 2), 
            'weight' : weight_interface
        })
        a = router_source[1]['label']
        a_ip_address = str(network[2]['network'].network_address + 1)
        b = router_target[1]['label']
        b_ip_address = str(network[2]['network'].network_address + 2)
        network_line = f'Network[{subnet.network_address}]\t[{a}({a_ip_address}) -> {b}({b_ip_address})] = {weight_interface:.2f} km\n'
        print(network_line)
        topology.write(network_line)

    title_router = "------------------------------------ Routers\n"
    print(title_router)
    topology.write(title_router)
    caracters_replace=[" ", "(", ")", ":", ",", ".", "ñ", "?", "¿","!", "¡"]
    lab = open(path_lab + '/lab.conf', 'w')
    for router in routers:
        machine_name = router[1]['label'].lower()
        print(machine_name)
        topology.write(machine_name + "\n")
        for caracter in caracters_replace:
            machine_name = machine_name.replace(caracter, "_")
        router[1]['label'] = machine_name
        id_machine = int(router[0])
        interface_index = 0
        commands_ospf = []
        startup = open(path_lab + "/" + machine_name + '.startup', 'w')
        for interface_router in interfaces[id_machine]:
            command = f"ifconfig eth{interface_index} {interface_router['ip_address']}/{network_gen_mask} up\n"
            startup.write(command)
            interface_label = interface_router['label']
            lab_command = f"{machine_name}[{interface_index}]={interface_label}\n"
            lab.write(lab_command)
            weight = int(interface_router['weight']) if int(interface_router['weight']) > 0 else 1
            command_ospf = f"interface eth{interface_index}\nospf cost {weight}\n"
            commands_ospf.append(command_ospf)
            interface_index += 1
        startup.write("\n/etc/init.d/quagga start") # add start quagga
        startup.close()

        route_machine = path_lab + "/" + machine_name

        if routing == "rip":
            copy_folder("files/rip",route_machine)
            with open(route_machine + "/" + file_rip, 'r+') as file:
                content = file.read()
                content_replace = content.replace(network_text, network_gen)
                file.seek(0)
                file.write(content_replace)
        if routing == "ospf":
            copy_folder("files/ospf", route_machine)
            with open(route_machine + "/" + file_ospfd, 'r+') as file:
                content = file.read()
                content_replace = content.replace(change_text, ''.join(commands_ospf))
                content_replace = content_replace.replace(network_text, network_gen)
                file.seek(0)
                file.write(content_replace)

        create_test_machine(path_test + "/" + machine_name + ".test", interfaces, id_machine)

    lab.close()
    topology.close()