# Prueba-Desarrollo
En este repositorio se encuentra la prueba de desarrollo elaborada para el cargo BISO en MeLi

# Instrucciones de ejecución
El programa fue construido, probado y ejecutado desde Python 3.11.7. 
Para ejecutar el código se debe ejecutar desde una ventana de comandos la siguiente sentencia:

$ python3 Prueba_Desarrollo.py

# Descripción del ejercicio
La finalidad de este programa es generar una base de datos a partir de correlacionar un archivo tipo JSON denominado "datos_json.json"
(el cuál contiene información de clasificación de las bases de datos, como "database","classification" y "owner")
y un archivo csv llamado "datos_csv.csv" (el cuál contiene información como el "row_id", "user_id", "user_state" y el "user_manager").

Por cada registro en ésta base de datos donde la clasificación sea alta (high), se enviará un emial al manager del owner
pidiendo su OK respecto a la clasificación.

# Supuestos, problemas y soluciones
De acuerdo a lo presentado dentro del ejercicio, se presentan algunos problemas que requieren supuestos para encontrar alguna solución al ejercicio:
## Problema 1: Relación entre los archivos JSON y CSV
A simple vista no existe alguna relación entre los datos contenidos entre el archivo JSON y el archivo CSV.
## Supuesto 1: "User_id" igual a "owner"
El "user_id" del archivo csv es el mismo "owner" dentro del archivo json.
## Problema 2: Datos incompletos dentro del archivo JSON
Dentro de la descripción del ejercicio no muestra qué datos podrían no estar dentro del JSON.
## Supuesto 2.1: Inexistencia de "database" o "classification" 
Si el dato de "database" o "classification" no está dentro del archivo JSON, ningún dato será insertado dentro de la base de datos.
## Supuesto 2.2: Inexistencia de "owner"
Si el dato de "owner" no está dentro del archivo JSON, se asigna un emial por defecto ("todero@gmail.com") el cuál también tendrá un manager asignado.
Esto contemplando la posibilidad que si una base de datos no contiene un owner y su clasificación es alta,
pueda ser verificada por el manager.


# Descripción de la solución
Dentro del programa denominado "Prueba_Desarrollo.py" se encuentran las siguientes funciones:

-cargar_datos_json: Se encarga de leer los datos del archivo json. Devuelve un archivo json.

-cargar_datos_csv: Se encarga de leer los datos del archivo csv y crea el diccionario relacionando el "user_id" con el "user_manager". Devuelve un diccionario.

-inicializacion_database: Crea la base de datos y la tabla de la base de datos si no existe y, de existir, elimina los datos para que no se acumulen. Devuelve un elemento "connection" y otro "cursor",

-insertar_datos_database: Inserta los datos en la base de datos a partir de un cursor, los datos del json y los datos del csv. 

-enviar emails: A partir de una consulta a la base de datos donde la clasificación sea alta ("classificaction=high") y si contiene el correo del manager, se enviará
un correo a la espera del "Ok" respecto a la clasificación de alta criticidad para la base de datos.

-main: Contiene el nombre de los archivos (JSON, csv, base de datos y el servidor, puerto, usuario, contraseña del smtp) y la invocación de las funciones anteriormente mencionadas. Todo esto con la finalidad de dar solución al ejercicio.
