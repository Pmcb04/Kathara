# Practica 2. TopologyZoo

En esta segunda práctica se seleccionará una topología de red de las librerías SNDLib o TopologyZoo y se creará un script que cree un laboratorio de Kathara de manera automática. Tras su ejecución, se realizará documentación de las diversas pruebas que permitan comprobar el funcionamiento de los protocolos RIP OSPF estudiados en clase. Se deben describir cada uno de los pasos realizados en una memoria técnica, además de entregar los archivos y los directorios de los laboratorios.

# Ejecución

```python

python3 main.py <Dataset> <Formato de archivo> <Protocolo de enrutamiento> <Ruta de la topologia>

cd generate/<Nombre de la topologia>

kathara lstart

# Para ejecutar los test
kathara ltest

```

# Argumentos validos

| Dataset                   | topologyzoo                                     |
|---------------------------|-------------------------------------------------|
| Formato de archivo        | gml                                             |
| Protocolo de enrutamiento | rip, ospf                                       |
| Ruta de la topologia      | Ejemplos en la carpeta topology/topologyzoo/gml |

# Estructura de ficheros

- **classes** (Clases utilizadas para el proyecto)
- **files** (Contiene las plantillas para el enrutamiento en RIP o OSPF)
- **generate** (Contendrá una carpeta por cada topología generada)
  - <Nombre de la topología> ( Archivos generados para la topología elegida)
- **parser** (Parser utilizados para pasar la topología)
- **topology** (Ficheros de las topologías)
- main.py (Archivo principal de ejecución)
