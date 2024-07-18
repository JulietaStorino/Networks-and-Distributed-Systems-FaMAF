# Tarea Estrella
Se pide investigar qué mecanismos permiten funcionar a nombres de dominio como:
- http://中文.tw/
- https://💩.la

    Ayuda: investigue sobre el término “encoding”.

## Definición de codificación (encoding)
Es el proceso a través del cual se transforma información textual humana, como *caracteres alfabéticos* (letras mayúsculas y minúsculas del alfabeto) y *no alfabéticos* (números, signos de puntuación, signos matemáticos, símbolos especiales, etc) en un conjunto más reducido, para ser almacenado o transmitido. 
En el mundo de las computadoras el codificación asocia nuestros signos alfabéticos y no alfabéticos con números binarios. Todos los signos que utilizamos al componer un texto en la computadora deben traducirse a estos números si queremos almacenarlos y/o transmitirlos. Para realizarlo, se acude a una *tabla de codificación* que mantiene la relación entre los caracteres en binario y su representación.

## Mecanismos de codificación famosos
### ISO-8859-1
Más conocido como Latin1, es una de las codificaciones *ASCII extendido* más comunes. Este tipo de codificación utiliza números de 8 bits para representar todos los signos. Es decir que todos los signos se transforman en un número entre el 0 y el 255 a partir de una especie de tabla predefinida. En este codificación, por ejemplo, nuestra letra *eñe* se transforma en el número 241 (11110001).

### UTF-8
Otra de las codificaciones más utilizadas, fuertemente recomendada y que se ha convertido en un estándar, ya que, a diferencia del anterior, no tiene una cantidad fija de bits para representar los caracteres. Utiliza un sistema de *largo variable* para lograr mayor flexibilidad. UTF-8 puede representar todos los caracteres de *Unicode*, un estándar creado a fines de los ochenta para codificar todos los caracteres de todas las lenguas escritas del mundo: un total de más de 100 mil signos.

## Codificación de URL
Es un mecanismo de codificación que convierte los caracteres en URLs a un formato válido, es decir, que se puede enviar a través de Internet. Existen caracteres reservados que tienen un significado determinado dentro de la ruta de datos y que no siempre se pueden codificar facilmente, estos son *! # $ % & ' ( ) * + , / : ; = ? @ [ ]*. Por ejemplo, # en una URL indica una marca de salto dentro de un sitio web, & marca una cadena de consulta y separa los parámetros individuales de la URL, y = especifica el valor de un parámetro.

También, hay momentos en los que necesita pasar caracteres que no son válidos para las URL, como *„ <  > { } \ | ^ ` y espacios*. Por ejemplo, el espacio en blanco no es un carácter de URL válido, ya que sería difícil ver la URL completa en textos con espacios en blanco. Aquí, la codificación de URL reemplaza los caracteres ASCII no válidos o reservados con un % seguido de dos dígitos hexadecimales. Por ejemplo, codifica "中文" como *%E4%B8%AD%E6%96%87* y "💩" como *%F0%9F%92%A9*

## Bibliografía
[FOROALFA - El misterioso mundo del encoding](https://foroalfa.org/articulos/el-misterioso-mundo-del-encoding#:~:text=El%20encoding%20(%C2%ABcodificaci%C3%B3n%C2%BB%20en,para%20ser%20almacenado%20o%20transmitido.))

[IBM - UCS-2 y UTF-8](https://www.ibm.com/docs/es/aix/7.3?topic=support-ucs-2-utf-8)

[Site24x7 - Codificador/Decodificador de URL](https://www.site24x7.com/es/tools/url-encoder-decoder.html#:~:text=%C2%BFQu%C3%A9%20es%20la%20codificaci%C3%B3n%20de,pueden%20enviar%20utilizando%20caracteres%20ASCII.)

[Ryte Wiki - URL Encoding](https://en.ryte.com/wiki/URL_Encoding)