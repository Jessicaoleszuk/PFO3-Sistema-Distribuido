# PFO 3 - Sistema distribuido cliente-servidor

## Objetivo
Implementar una comunicación cliente-servidor mediante sockets TCP en Python. El servidor recibe tareas en formato JSON, las distribuye a un pool de workers (hilos) y devuelve el resultado al cliente.

## Archivos
- `servidor.py`: servidor TCP y pool de workers.
- `cliente.py`: cliente que envía tareas y recibe respuestas.
- `diagrama.md`: diagrama de arquitectura y descripción de los componentes.

## Requisitos
- Python 3.10 o superior.
- No requiere instalar librerías externas: usa módulos incluidos en Python.

## Cómo ejecutar en Windows
1. Descargá y descomprimí el proyecto.
2. Abrí la carpeta en Visual Studio Code.
3. Abrí una terminal y ejecutá:

   ```bash
   python servidor.py
   ```

4. Dejá esa terminal abierta. Abrí una segunda terminal en la misma carpeta y ejecutá:

   ```bash
   python cliente.py
   ```

5. Elegí una opción y seguí las instrucciones. Para probar varias solicitudes, volvé a ejecutar `python cliente.py` en la segunda terminal.

El servidor escucha en `127.0.0.1:5000`. Esta dirección permite probar ambos programas en la misma computadora.

## Ejemplos de tareas
- `saludar`: devuelve un saludo personalizado.
- `sumar`: suma dos números.
- `mayusculas`: convierte un texto a mayúsculas.

## Cómo funciona
1. El cliente crea una conexión TCP con el servidor.
2. Envía una tarea codificada como JSON y terminada en un salto de línea.
3. El servidor recibe el mensaje y envía la tarea al pool de workers.
4. Un hilo procesa la tarea.
5. El servidor devuelve una respuesta JSON y el cliente la muestra.

## Pruebas sugeridas
- Probar las tres opciones del menú.
- Ingresar letras cuando se solicitan números para comprobar la validación.
- Ejecutar varios clientes en distintas terminales para observar cómo se atienden varias conexiones.

## Arquitectura ampliada
El archivo `diagrama.md` muestra Nginx/HAProxy, RabbitMQ, PostgreSQL y S3. Estos componentes forman parte del diseño propuesto, pero no están desplegados ni conectados en esta demostración. La implementación funcional del PFO se concentra en sockets TCP, concurrencia con hilos y distribución de tareas a workers.

## Subir el proyecto a GitHub
1. Ingresá a https://github.com y creá un repositorio nuevo llamado `PFO3-Sistema-Distribuido`.
2. No hace falta agregar README desde GitHub, porque el proyecto ya incluye uno.
3. En la página del repositorio, elegí **Add file > Upload files**.
4. Subí `servidor.py`, `cliente.py`, `diagrama.md` y `README.md`.
5. Confirmá con **Commit changes**.
6. Copiá el enlace del repositorio para compartirlo como entrega.
