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

## Práctica 1
En esta practica se pedía conectar 4 redes (_pc-net, ws-net, x-net-1 e internet_) a 3 routers (_A, B, C_), configurar perfectamente sus tablas de rutas para que haya conectividad total y establecer una serie de pruebas para comprobar esa conectividad total.

## Práctica 2
En esta segunda práctica se seleccionará una topología de red de las librerías [SNDLib](http://sndlib.zib.de/home.action) o [TopologyZoo](http://www.topology-zoo.org/) y se creará un script que cree un laboratorio de Kathará de manera automática. Tras su ejecución, se realizarán y documentarán diversas pruebas que permitan comprobar el funcionamiento de los protocolos RIP y OSPF estudiados en clase. Se deben describir cada uno de los pasos realizados en una memoria técnica, además de entregar los archivos y los directorios de los laboratorios.