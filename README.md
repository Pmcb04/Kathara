# Kathara
Practicas realizadas durante la asignatura de  Tecnologías y Protocolos de Comunicación (2023)


# Instalación en ubuntu

```bash
sudo add-apt-repository ppa:katharaframework/kathara

sudo apt update

sudo apt install kathara xterm
```

# Laboratorios

## Lab 0
Realización de la primera red con 3 PC's (_pc1, pc2, pc3_) en donde _pc2_ tiene dos interfaces _ethernet_ y hace de mediadora entre las dos redes definidas.

## Lab 1
Realización de un escenario de dos host (_pc1, pc2_) y hacer PING uno a otro para ver como se captura el tráfico de la red con el comando _tcpdumb_
## Lab 2
Escenario de 3 redes y dos routers (_r1, r2_), teniendo un pc en dos redes (_pc1 y pc2_). Aqui se hace practica del encaminamiento estático para poder enlazar redes y hacer correctamente el encaminamiento

## Lab 3
Realización de la primera red con 3 PC's (_pc1, pc2, pc3_) en donde se hace practica de el protocolo de encaminamiento de _ARP_, se pueden ver como van hablando los distintos pc's y llenando su tabla _ARP_

## Lab 4 
Realización de topologías con varias redes en donde un subconjunto del total de redes habla protocolo _RIP_ y el otro no. Se observa como se van intercambiando los mensajes de este protocolo en el tiempo los diferentes host que lo componen.

## Lab 5
Realización de una topología para poder ver el funcionamiento de el protocol OSPF y ver como se calculan las rutas en función del coste de los enlaces, tambien se hace la prueba de eliminar un enlace y recalcular las rutas, siempre por el camino más corto.


# Prácticas

## Kathara

### Práctica 1
En esta practica se pedía conectar 4 redes (_pc-net, ws-net, x-net-1 e internet_) a 3 routers (_A, B, C_), configurar perfectamente sus tablas de rutas para que haya conectividad total y establecer una serie de pruebas para comprobar esa conectividad total.

### Práctica 2
En esta segunda práctica se seleccionará una topología de red de las librerías [SNDLib](http://sndlib.zib.de/home.action) o [TopologyZoo](http://www.topology-zoo.org/) y se creará un script que cree un laboratorio de Kathará de manera automática. Tras su ejecución, se realizarán y documentarán diversas pruebas que permitan comprobar el funcionamiento de los protocolos RIP y OSPF estudiados en clase. Se deben describir cada uno de los pasos realizados en una memoria técnica, además de entregar los archivos y los directorios de los laboratorios.

## Mininet

###  Practica 3 

La red no tiene un controlador definido. Conceptualmente, existen dos redes privadas: la red
10.0.1.0/24 a la que pertenecen los hosts H1, H2 y H3; y la red 10.0.2.0/24 a la que pertenecen
los hosts H4, H5 y H6. Ambas redes privadas están conectadas a través de una red pública que
está representada por los switches S1, S2, S3 y el host H7.
La capacidad de los enlaces que conectan los switches es de 10 Mbps cada uno. Además, en el
host H7 existe un servidor web en ejecución. Se pide:
1. Asignar las direcciones IP a los hosts de manera coherente según el esquema descrito.
2. Crear un script Python que genere la topología de red descrita.
3. Utilizar el pipeline normal para cada tipo de tráfico en el switch S2.
4. Configurar los switches S1 y S3 de modo que se satisfagan los siguientes puntos:
a. En el interior de cada red privada, los hosts se deben comunicar entre sí.
b. El tráfico que va desde la red 10.0.1.0/24 hacia la red 10.0.2.0/24 debe pasar
por la red pública utilizando direcciones IP públicas (función NAT) 87.13.148.68
para la dirección IP origen y 87.100.12.18 para la dirección IP destino y
viceversa.
c. Los hosts de la red 10.0.2.0/24 no se deben poder comunicar con el servidor
web.
d. El host H1 es el único de la red 10.0.1.0/24 que puede abrir una conexión SSH
con el host eH4 (todo el tráfico SSH entre el resto de hosts debe descartarse)
Para la configuración de los tres switches se deben crear tres archivos de texto que contengan
las reglas de flujo. Se deben describir cada uno de los pasos realizados en una memoria técnica,
además de entregar todos los archivos necesarios