# Análisis de Tráfico y Control de Congestión en capa de Transporte mediante Simulaciones Discretas con OMNeT++

#### Autores:

- Courel Daniela
- Murphy Ronnie
- Storino Julieta

## Resumen

Este trabajo se enfoca en analizar la eficiencia y la pérdida de paquetes en un modelo de transmisión en OMNeT++. En primer lugar, se ha evaluado un modelo de colas inicial que consta de un generador, una cola y un destino. A través de experimentos con diferentes parámetros, se han identificado las limitaciones del sistema.

Con el fin de abordar el problema de congestión, se ha propuesto un nuevo diseño que incorpora control de congestión y flujo. Posteriormente, se han llevado a cabo simulaciones para evaluar la efectividad de esta solución.

## Introducción:

El objetivo de este estudio es evaluar el comportamiento de un modelo de colas en un entorno simulado en OMNeT++, una herramienta ampliamente utilizada para la simulación de sistemas de comunicación.

Al diseñar una red de transmisión de datos, es fundamental considerar aspectos como el control de flujo y el control de congestión.

El control de flujo se refiere a regular la velocidad de transmisión de datos entre un emisor y un receptor para evitar la sobrecarga del receptor y minimizar la pérdida de datos. En cambio, el control de congestión se trata de gestionar el flujo de datos en toda la red, incluyendo la detección y prevención de situaciones de congestión que puedan resultar en la pérdida de paquetes y una disminución en el rendimiento general de la red.

En este trabajo, el objetivo principal es analizar el comportamiento del sistema de colas en diferentes condiciones y diseñar estrategias efectivas de control de flujo y congestión para mejorar su rendimiento. Para lograr este objetivo, se plantean los siguientes pasos:

- Analizar el impacto de la capacidad de transferencia de datos y la memoria de buffers en el tráfico de red en un sistema básico.
- Diseñar e implementar estrategias de control de flujo y congestión para evitar la pérdida de datos por saturación de buffers.
- Evaluar el rendimiento del sistema mediante simulaciones en OMNeT++ y analizar los resultados obtenidos.

## Modelo Inicial:

Nuestro diseño inicial se basa en un sistema de colas que consta de un generador y un receptor conectados a través de un nodo intermedio.

<p align="center">
  <img src="images/output.png" alt="Modelo Inicial">
</p>

En nuestro sistema, los módulos NodeTx y NodeRx actúan como el emisor y receptor respectivamente.

- `NodeTx`: Este módulo incluye un emisor de paquetes y una cola. El generador produce paquetes de tamaño fijo de *12500 bytes* y los envía a la cola a intervalos regulares, siguiendo una distribución exponencial centrada en *T*. La cola se encarga de enviar los paquetes al nodo intermedio.

- `NodeRx` También consta de una cola y un receptor de paquetes. El receptor recibe los paquetes y los procesa a una velocidad constante. La cola almacena temporalmente los paquetes hasta que el receptor los consume, descartándolos si la cola se llena.

- `Cola Intermedia` El buffer de la cola intermedia tiene capacidad para *200* paquetes y se encarga de almacenar los paquetes generados, enviándolos a la velocidad determinada por una distribución exponencial centrada en *Q* hacia el receptor. Si el buffer alcanza su capacidad máxima, los paquetes excedentes se descartan.
