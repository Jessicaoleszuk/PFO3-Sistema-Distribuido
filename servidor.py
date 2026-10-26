import json
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000
CANTIDAD_WORKERS = 4

# Pool de hilos: permite procesar varias tareas concurrentemente.
pool_workers = ThreadPoolExecutor(max_workers=CANTIDAD_WORKERS)


def procesar_tarea(tarea):
    """Función de ejemplo que simula el trabajo de un worker."""
    accion = tarea.get("accion", "saludar")
    datos = tarea.get("datos", {})

    if accion == "saludar":
        nombre = datos.get("nombre", "usuario")
        resultado = f"Hola, {nombre}. La tarea fue procesada correctamente."
    elif accion == "sumar":
        try:
            a = float(datos["a"])
            b = float(datos["b"])
            resultado = f"Resultado de la suma: {a + b:g}"
        except (KeyError, TypeError, ValueError):
            resultado = "Error: para sumar se necesitan los datos numericos 'a' y 'b'."
    elif accion == "mayusculas":
        texto = str(datos.get("texto", ""))
        resultado = texto.upper()
    else:
        resultado = f"Accion no reconocida: {accion}"

    return {
        "estado": "ok",
        "resultado": resultado,
        "worker": threading.current_thread().name,
        "fecha": datetime.now().isoformat(timespec="seconds")
    }


def recibir_mensaje(conexion):
    """Lee un mensaje JSON terminado en salto de línea."""
    buffer = b""
    while b"\n" not in buffer:
        fragmento = conexion.recv(4096)
        if not fragmento:
            break
        buffer += fragmento
        if len(buffer) > 1_000_000:
            raise ValueError("El mensaje supera el tamaño permitido.")
    if not buffer:
        return None
    linea = buffer.split(b"\n", 1)[0]
    return json.loads(linea.decode("utf-8"))


def atender_cliente(conexion, direccion):
    print(f"[NUEVA CONEXION] Cliente conectado desde {direccion}")
    with conexion:
        try:
            tarea = recibir_mensaje(conexion)
            if tarea is None:
                return

            if not isinstance(tarea, dict):
                raise ValueError("La tarea debe ser un objeto JSON.")

            print(f"[TAREA RECIBIDA] {tarea}")

            # Se envía la tarea al pool de workers y se espera el resultado.
            futuro = pool_workers.submit(procesar_tarea, tarea)
            respuesta = futuro.result()

        except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as error:
            respuesta = {"estado": "error", "resultado": str(error)}
        except Exception as error:
            respuesta = {"estado": "error", "resultado": f"Error interno: {error}"}

        try:
            conexion.sendall((json.dumps(respuesta, ensure_ascii=False) + "\n").encode("utf-8"))
        except OSError:
            print(f"[AVISO] No se pudo enviar respuesta a {direccion}")

    print(f"[CONEXION CERRADA] {direccion}")


def iniciar_servidor():
    print(f"[SERVIDOR] Escuchando en {HOST}:{PORT}")
    print(f"[WORKERS] Pool configurado con {CANTIDAD_WORKERS} hilos")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORT))
        servidor.listen()
        try:
            while True:
                conexion, direccion = servidor.accept()
                hilo = threading.Thread(
                    target=atender_cliente,
                    args=(conexion, direccion),
                    daemon=True
                )
                hilo.start()
        except KeyboardInterrupt:
            print("\n[SERVIDOR] Cerrando servidor...")
        finally:
            pool_workers.shutdown(wait=True)


if __name__ == "__main__":
    iniciar_servidor()
