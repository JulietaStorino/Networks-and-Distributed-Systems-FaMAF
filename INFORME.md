# Análisis de Tráfico y Control de Congestión en capa de Transporte mediante Simulaciones Discretas con OMNeT++

#### Autores:

- Courel Daniela
- Murphy Ronnie
- Storino Julieta

## Resumen

Este trabajo se realiza en el marco de la cátedra de Redes y Sistemas Distribuidos con el objetivo de leer, comprender y generar modelos de red en Omnet++, analizando el tráfico y  proponiendo soluciones de control de congestión y flujo en la capa de transporte bajo tasas de datos acotadas y tamaño de buffers limitados.
En primer lugar, se ha evaluado mediante simulaciones un modelo de colas inicial que consta de un generador (generator), una cola (queue) y un destino (sink) a manera de identificar las limitaciones del sistema.
Posteriormente, se ha propuesto un nuevo diseño que incorpora control de congestión y flujo, con el fin de abordar el problema hallado de congestión.
Finalmente, se han llevado a cabo simulaciones para evaluar la efectividad de esta solución.

## Introducción:

Al diseñar una red de transmisión de datos, es fundamental considerar aspectos como el control de flujo y el control de congestión para garantizar un rendimiento óptimo y evitar la pérdida de paquetes. Para esto recurrimos a la simulación de sistemas de comunicación, que nos permite evaluar el comportamiento de la red en diferentes condiciones y diseñar estrategias efectivas para mejorarlas.

De esta manera, el objetivo de este trabajo es evaluar el comportamiento de un modelo de colas en un entorno simulado en OMNeT++, una herramienta ampliamente utilizada para la simulación de sistemas de comunicación.

En particular, nos centraremos en el análisis del tráfico de red y el diseño de estrategias de control de flujo y congestión para mejorar el rendimiento del sistema. El primero refiere a regular la velocidad de transmisión de datos entre un emisor y un receptor para evitar la sobrecarga del receptor y minimizar la pérdida de datos. En cambio, el control de congestión se trata de gestionar el flujo de datos en toda la red, incluyendo la detección y prevención de situaciones de congestión que puedan resultar en la pérdida de paquetes y una disminución en el rendimiento general de la red.

Para cumplir con los objetivos propuestos, se plantean los siguientes pasos:

- Analizar el impacto de la capacidad de transferencia de datos y la memoria de buffers en el tráfico de red en un sistema básico.
- Diseñar e implementar estrategias de control de flujo y congestión para evitar la pérdida de datos por saturación de buffers.
- Evaluar el rendimiento del sistema mediante simulaciones en OMNeT++ y analizar los resultados obtenidos.

## Métodos
### Modelo Inicial:

Nuestro diseño inicial se basa en un sistema de colas que consta de un generador y un receptor conectados a través de un nodo intermedio.

<p align="center">
  <img src="images/output.png" alt="Modelo Inicial">
</p>

En nuestro sistema, los módulos NodeTx y NodeRx actúan como el emisor y receptor respectivamente.

- `NodeTx`: Este módulo incluye un emisor de paquetes y una cola. El generador produce paquetes de tamaño fijo de *12500 bytes* y los envía a la cola a intervalos regulares, siguiendo una distribución exponencial centrada en *T*. La cola se encarga de enviar los paquetes al nodo intermedio.

- `NodeRx` También consta de una cola y un receptor de paquetes. El receptor recibe los paquetes y los procesa a una velocidad constante. La cola almacena temporalmente los paquetes hasta que el receptor los consume, descartándolos si la cola se llena.

- `Cola Intermedia` El buffer de la cola intermedia tiene capacidad para *200* paquetes y se encarga de almacenar los paquetes generados, enviándolos a la velocidad determinada por una distribución exponencial centrada en *Q* hacia el receptor. Si el buffer alcanza su capacidad máxima, los paquetes excedentes se descartan.

### Detalles de simulación del Modelo Inicial:
Para analizar el modelo inicial, realizamos varias configuraciones. Primero, establecemos el nombre de la red que vamos a simular. Segundo, ponemos un límite al tiempo de simulación, fijándolo en 200 segundos. Luego, procedemos a configurar los parámetros de los módulos de la red. Establecemos el tiempo de servicio de la cola en la red, en el nodo de transmisión y en el nodo de recepción. Este tiempo de servicio se define como una distribución exponencial con una media de 0.001. Además, definimos el intervalo de generación en el nodo de transmisión también como una distribución exponencial, pero con una media de 0.1. Finalmente, configuramos el tamaño del buffer en la cola del nodo de transmisión, estableciéndolo en 2000000.

Así podemos presentar dos casos de estudio que se centran en variar la tasa de datos en las conexiones de salida de la cola en los módulos. En el primer caso de estudio, la tasa de datos se establece en 0.5 Mbps. Esto representa una situación en la que la red tiene una capacidad de transmisión de datos relativamente baja. En el segundo caso de estudio, la tasa de datos se incrementa a 1 Mbps. Este caso representa una situación en la que la red tiene una mayor capacidad de transmisión de datos. Es importante destacar que, aparte de la tasa de datos, todos los demás parámetros se mantienen constantes en ambos casos de estudio. Esto permite que cualquier diferencia observada en el comportamiento de la red pueda atribuirse directamente a la variación en la tasa de datos.

### Simulación del Modelo Inicial:
<p align="center">
  <img src="https://i.ibb.co/XyV8Xfd/Packet-Drop-in-Network-Node-Rx-Queue.png" alt="Packet-Drop-in-Network-Node-Rx-Queue">
</p>

<p align="center">
  <img src="https://i.ibb.co/zsnGGYW/Number-Of-Packets-in-Network-Node-Rx-Sink.png" alt="Number-Of-Packets-in-Network-Node-Rx-Sink">
</p>

<p align="center">
  <img src="https://i.ibb.co/m6q0gwR/Delay-in-Network-Node-Rx-Sink.png" alt="Delay-in-Network-Node-Rx-Sink">
</p>

<p align="center">
  <img src="https://i.ibb.co/L9kzLhF/Buffer-Size-in-Network-Queue.png" alt="Buffer-Size-in-Network-Queue">
</p>

<p align="center">
  <img src="https://i.ibb.co/k66x6c4/Buffer-Size-in-Network-Node-Tx-Queue.png" alt="Buffer-Size-in-Network-Node-Tx-Queue">
</p>

<p align="center">
  <img src="https://i.ibb.co/M2hsvTs/Buffer-Size-in-Network-Node-Rx-Queue.png" alt="Buffer-Size-in-Network-Node-Rx-Queue">
</p>

<p align="center">
  <img src="https://i.ibb.co/7YBjqw9/Average-Delay-in-Network-Node-Rx-Sink.png" alt="Average-Delay-in-Network-Node-Rx-Sink">
</p>





