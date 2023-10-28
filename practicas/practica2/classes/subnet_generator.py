import ipaddress

class SubnetGenerator:
    def __init__(self, start_ip, subnet_mask):
        self.start_ip = ipaddress.IPv4Address(start_ip)
        self.subnet_mask = subnet_mask

    def get_next_subnet(self):
        subnet = ipaddress.IPv4Network(f"{self.start_ip}/{self.subnet_mask}", strict=False)
        self.start_ip = self.increment_ip(self.start_ip)
        return subnet

    def increment_ip(self, ip):
        # Convierte la dirección IP a un número entero
        ip_int = int(ip)
        # Incrementa la dirección IP en 1
        ip_int += 4
        # Convierte el número entero de nuevo a una dirección IP
        return ipaddress.IPv4Address(ip_int)