import re
from classes import node,link,demand
import xml.etree.ElementTree as ET


class SNDLibNativeParser:
    def __init__(self, data):
        self.data = data

    def parse_sections(self):
        sections = re.split(r'\n(?=\w+\s*\()', self.data)
        section_dict = {}
        for section in sections:
            lines = section.strip().split('\n')
            section_name = lines[0].strip()
            section_data = '\n'.join(lines[1:]).strip()
            section_dict[section_name] = section_data
        return section_dict

    def parse_meta_section(self):
        meta_section = self.sections.get('META', '')
        meta_info = {}
        for line in meta_section.split('\n'):
            if '=' in line:
                key, value = [item.strip() for item in line.split('=')]
                meta_info[key] = value
        return meta_info

    def parse_nodes_section(self):
        nodes_section = self.sections.get('NODES', '')
        nodes_info = {}
        for line in nodes_section.split('\n'):
            if line.strip():
                node_data = line.strip().split()
                node_id, coordinates = node_data[0], tuple(map(float, node_data[1:]))
                nodes_info[node_id] = coordinates
        return nodes_info

    def parse_links_section(self):
        links_section = self.sections.get('LINKS', '')
        links_info = {}
        for line in links_section.split('\n'):
            if line.strip():
                link_data = line.strip().split()
                link_id, source, target = link_data[0], link_data[1], link_data[2]
                capacity, cost, routing_cost, setup_cost = map(float, link_data[3:7])
                module_info = link_data[8:]
                links_info[link_id] = {
                    'source': source,
                    'target': target,
                    'capacity': capacity,
                    'cost': cost,
                    'routing_cost': routing_cost,
                    'setup_cost': setup_cost,
                    'module_info': module_info
                }
        return links_info

    def parse_demands_section(self):
        demands_section = self.sections.get('DEMANDS', '')
        demands_info = {}
        for line in demands_section.split('\n'):
            if line.strip():
                demand_data = line.strip().split()
                demand_id, source, target = demand_data[0], demand_data[1], demand_data[2]
                routing_unit, demand_value, max_path_length = map(float, demand_data[3:6])
                demands_info[demand_id] = {
                    'source': source,
                    'target': target,
                    'routing_unit': routing_unit,
                    'demand_value': demand_value,
                    'max_path_length': max_path_length
                }
        return demands_info

    def parse_admissible_paths_section(self):
        admissible_paths_section = self.sections.get('ADMISSIBLE_PATHS', '')
        admissible_paths = {}
        if admissible_paths_section.strip():
            demand_paths = admissible_paths_section.split('\n')
            for demand_path in demand_paths:
                demand_id, path_data = demand_path.split(' ( ')
                path_data = path_data.rstrip(')')
                path_ids = path_data.split()
                admissible_paths[demand_id] = path_ids
        return admissible_paths

    def parse(self):
        self.sections = self.parse_sections()
        self.meta_info = self.parse_meta_section()
        self.nodes_info = self.parse_nodes_section()
        self.links_info = self.parse_links_section()
        self.demands_info = self.parse_demands_section()
        self.admissible_paths = self.parse_admissible_paths_section()

class SNDLibXMLParser:
    def __init__(self, xml_file):
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()

    def parse_metadata(self):
        meta = self.root.find('.//meta')
        version = self.root.attrib['version']
        granularity = meta.find('granularity').text
        time = meta.find('time').text
        unit = meta.find('unit').text
        origin = meta.find('origin').text
        return {
            "Version": version,
            "Granularity": granularity,
            "Year": time,
            "Unit": unit,
            "Origin": origin
        }

    def parse_nodes(self):
        nodes = self.root.find('.//nodes')
        node_data = []
        for node in nodes.findall('node'):
            node_id = node.get('id')
            x = node.find('coordinates/x').text
            y = node.find('coordinates/y').text
            node_data.append({
                "Node ID": node_id,
                "Coordinates": (x, y)
            })
        return node_data

    def parse_links(self):
        links = self.root.find('.//networkStructure')
        link_data = []
        for link in links.findall('links/link'):
            link_id = link.get('id')
            source = link.find('source').text
            target = link.find('target').text
            capacity = link.find('preInstalledModule/capacity').text
            cost = link.find('preInstalledModule/cost').text
            link_data.append({
                "Link ID": link_id,
                "Source": source,
                "Target": target,
                "Capacity": capacity,
                "Cost": cost
            })
        return link_data

    def parse_demands(self):
        demands = self.root.find('.//demands')
        demand_data = []
        for demand in demands.findall('demand'):
            demand_id = demand.get('id')
            source = demand.find('source').text
            target = demand.find('target').text
            demand_value = demand.find('demandValue').text
            demand_data.append({
                "Demand ID": demand_id,
                "Source": source,
                "Target": target,
                "Demand Value": demand_value
            })
        return demand_data
