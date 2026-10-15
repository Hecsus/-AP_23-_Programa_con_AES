# AP 23 - Programa con AES

**Bootcamp Ciberseguridad · MF0489_3 · AP23**

Práctica en Python para comparar los modos de operación **AES-ECB** y **AES-CTR**, usando claves de **128 y 256 bits**.

## Archivos

- **ap23_aes.py**: programa principal; realiza las dos partes de la actividad y muestra los tamaños.
- **test_ap23.py**: pruebas automáticas con distintos tamaños de mensaje.
- **requirements.txt**: librería necesaria (PyCryptodome).
- **.gitignore**: excluye archivos generados por Python y entornos virtuales.

## Instalación y ejecución en VS Code (Windows)

Con Python instalado, abrir la terminal de VS Code en la carpeta del repositorio y ejecutar:

~~~powershell
python -m pip install -r requirements.txt
python ap23_aes.py
~~~

Para ejecutar las comprobaciones:

~~~powershell
python -m unittest -v
~~~

El programa pide el mensaje mediante input(). Lo convierte a UTF-8 y muestra el texto cifrado en hexadecimal (hex) para poder leerlo en la terminal.

## Parte 1 - AES.MODE_CTR con clave de 128 bits

Se parte de la clave de 16 bytes facilitada por el profesor.

**¿Qué ocurre si intentamos cifrar el texto plano?**

- En **ECB sin padding**, si el texto plano no tiene una longitud múltiplo de 16 bytes, se produce un ValueError.
- El programa añade bytes nulos (0x00) hasta completar bloques de 16 bytes y entonces ECB funciona.
- En **CTR**, el cifrado funciona sin añadir padding aunque el texto no mida un múltiplo de 16 bytes.

**¿Cuál es el tamaño del texto cifrado resultante?**

En CTR, la longitud del texto cifrado es **igual a la longitud del texto plano en bytes**. En ECB, después del padding de esta práctica, se redondea al siguiente múltiplo de 16 bytes (si ya era múltiplo, queda igual).

Ejemplo con el mensaje **Hola Bob**, que tiene 8 bytes en UTF-8:

| Datos | Tamaño |
| --- | ---: |
| Texto plano | 8 bytes |
| AES-128 ECB, con padding | 16 bytes |
| AES-128 CTR, sin padding | 8 bytes |

**Nota:** El nonce del modo CTR es un dato adicional necesario para descifrar y no está incluido en el tamaño de la salida cifrada mostrado en la tabla.

## Parte 2 - AES con clave de 256 bits

Se genera una nueva clave aleatoria de **32 bytes = 256 bits** con get_random_bytes(32). La clave de la Parte 1 contiene **16 bytes = 128 bits**.

**¿Qué diferencias hay en el tamaño del texto cifrado entre ECB y CTR?**

El tamaño de la clave **no modifica** el tamaño del bloque de AES, que siempre es de **16 bytes = 128 bits**.

| Mensaje de 8 bytes | AES-128 | AES-256 |
| --- | ---: | ---: |
| ECB con padding nulo | 16 bytes | 16 bytes |
| CTR sin padding | 8 bytes | 8 bytes |

Por tanto, ECB sigue necesitando completar bloques y CTR conserva el tamaño del mensaje, independientemente de que la clave tenga 128 o 256 bits.

El contenido hexadecimal de las salidas sí es diferente cuando cambia la clave. En CTR también cambia al usar un nonce distinto.

## Seguridad y observaciones

- **ECB no se recomienda para proteger información real**: si dos bloques de texto plano son iguales bajo la misma clave, sus bloques cifrados también lo son.
- El padding con bytes nulos se utiliza para reproducir el ejemplo de clase. Puede ser ambiguo al descifrar si el mensaje original acaba en ceros; en aplicaciones con padding conviene usar un esquema definido, como PKCS#7.
- **CTR requiere un nonce único por cada cifrado con la misma clave**. Reutilizar clave y nonce reutiliza el keystream, comprometiendo la confidencialidad.
- CTR proporciona confidencialidad, **no autenticidad ni integridad** por sí solo. Para datos reales puede utilizarse un esquema autenticado, como AES-GCM.
- La clave de 128 bits que figura en el código es la facilitada para la actividad; **no debe reutilizarse para información privada**. La clave de 256 bits se genera aleatoriamente en cada ejecución.

## Conclusión

Se ha comprobado que **ECB requiere bloques completos de 16 bytes**, mientras que **CTR puede cifrar cualquier longitud sin padding**. Cambiar la longitud de clave de 128 a 256 bits no cambia el tamaño del texto cifrado: únicamente cambia el tamaño de la clave, el número de rondas AES y sus propiedades de seguridad.
