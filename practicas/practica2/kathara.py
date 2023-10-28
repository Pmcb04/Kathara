import sys
import json
import signal
import subprocess
from Kathara.model.Lab import Lab
from Kathara.manager.Kathara import Kathara
from Kathara.setting.Setting import Setting

class KatharaLabManager:
    def __init__(self, lab_name):
        self.kathara = Kathara.get_instance()
        self.lab = Lab(lab_name)

    def connect(self, machine, lab):
        command = "%s -c \"from Kathara.manager.Kathara import Kathara; " \
                  "Kathara.get_instance().connect_tty(lab_hash='%s', machine_name='%s', shell='%s')\"" \
                  % (sys.executable, machine.lab.hash, machine.name, Setting.get_instance().device_shell)
        subprocess.Popen([Setting.get_instance().terminal, "-e", command], start_new_session=True)

    def connect_all(self):
        stats = self.get_lab_stats()

        for key, machine_stats in stats.items():
            machine_stats = machine_stats.to_dict()
            self.connect(self.get_machine(machine_stats["name"]), self.lab)

    def create_machine(self, machine_name, image):
        self.lab.new_machine(name=machine_name, kwargs=image)
    
    def get_machine(self, machine_name):
        return self.lab.get_machine(machine_name)

    def startup_file(self, machine_name, rules):
        # Configure router1 startup commands
        self.lab.create_file_from_list(
            rules,
            machine_name + ".startup"
        )

    def create_network(self, network_name):
        self.lab.new_link(network_name)

    def connect_to_network(self, machine_name, network_name):
        self.lab.connect_machine_to_link(machine_name, network_name)

    def create_file_from_string(self, content, pathHost, machine_name):
        self.get_machine(machine_name).create_file_from_string(content=content, dst_path=pathHost)
    
    def create_file_from_path(self, pathLocal, pathHost, machine_name):
        self.get_machine(machine_name).create_file_from_path(pathLocal, pathHost)

    def undeploy_lab(self):
        self.kathara.undeploy_lab(lab_name=self.lab.name)
        print("Laboratorio", self.lab.name, " eliminado correctamente")

    def get_lab_stats(self):
        return next(self.kathara.get_machines_stats(lab_name=self.lab.name))

    def print_stats(self):
        stats = self.get_lab_stats()
        print()
        for key, machine_stats in stats.items():
            machine_stats = machine_stats.to_dict() 
            print("---------------------------------------")
            print("name : ", machine_stats["name"])
            print("container_name : ", machine_stats["container_name"])
            print("user : ", machine_stats["user"])
            print("network_scenario_id : ", machine_stats["network_scenario_id"])
            print("---------------------------------------")
            print()

    def run(self):
        try:
            print(self.kathara.get_lab_from_api(lab_name=self.lab.name))
            self.kathara.deploy_lab(self.lab)
            self.print_stats()
            print("Laboratorio", self.lab.name, "desplegado correctamente")
            # self.print_stats()
            while True:
                command = input("Ingrese una orden: ")

                if command.lower() == "connect all":
                    print("Conectando todos los dispositivos...")
                    self.connect_all()
                elif command.lower().startswith("connect "):
                    machine_name = command[8:]  # Para obtener el nombre después de "connect "
                    print(f"Conectando a: {machine_name}")
                    self.connect(self.get_machine(machine_name), self.lab)
                elif command.lower() == "exit":
                    print("Saliendo del programa.")
                    self.undeploy_lab()
                    sys.exit(0)
                    break 
                else:
                    print("Orden no reconocida. Intente de nuevo.")
        except KeyboardInterrupt:
            pass

    def exit():
        self.custom_action()
        sys.exit(0)