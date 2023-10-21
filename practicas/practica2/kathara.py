from Kathara.model.Lab import Lab
from Kathara.manager.Kathara import Kathara
from Kathara.setting.Setting import Setting
import signal
import sys
import os
import shutil
import subprocess

kathara=Kathara.get_instance()

def connect(machine, lab):
    print("aqui")
    command = "%s -c \"from Kathara.manager.Kathara import Kathara; " \
          "Kathara.get_instance().connect_tty(lab_hash='%s', machine_name='%s',shell='%s')\"" \
          % (sys.executable, machine.lab.hash, machine.name, Setting.get_instance().device_shell)
    subprocess.Popen([Setting.get_instance().terminal, "-e", command], start_new_session=True)
    print('alli')

def custom_action():
    # Define aquí la acción que deseas ejecutar antes de salir.
    print("Ejecutando acción antes de salir...")
    kathara.undeploy_lab(lab_name=lab.name)
    # Puedes agregar más acciones aquí.

def sigint_handler(sig, frame):
    # Esta función se ejecutará cuando se presione Control + C.
    print("Se ha presionado Control + C. Saliendo...")
    custom_action()  # Ejecuta la acción personalizada antes de salir.
    sys.exit(0)

# Asigna el manejador de señal SIGINT
signal.signal(signal.SIGINT, sigint_handler)

try:
    lab = Lab("my lab")
    h1 = lab.get_or_new_machine('h1')
    lab.connect_machine_to_link('h1', 'A', 0)
    kathara.wipe()
    kathara.deploy_lab(lab)

    # Call custom connect function passing the machine
    connect(h1, lab)
    # kathara.connect_tty(lab_name=lab.name, machine_name=h1.name)
    
    while True:
        pass
except KeyboardInterrupt:
    # Esto se ejecutará si se presiona Control + C.
    pass
