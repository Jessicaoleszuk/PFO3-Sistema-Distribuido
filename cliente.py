import json
import socket

HOST = "127.0.0.1"
PORT = 5000


def enviar_tarea(tarea):
    """Conecta con el servidor, envía una tarea JSON y recibe la respuesta."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.settimeout(10)
        cliente.connect((HOST, PORT))
        mensaje = json.dumps(tarea, ensure_ascii=False) + "\n"
        cliente.sendall(mensaje.encode("utf-8"))

        buffer = b""
        while b"\n" not in buffer:
            parte = cliente.recv(4096)
            if not parte:
                break
            buffer += parte

        if not buffer:
            print("El servidor cerró la conexión sin responder.")
            return

        respuesta = json.loads(buffer.split(b"\n", 1)[0].decode("utf-8"))
        print("\n--- Respuesta del servidor ---")
        print(json.dumps(respuesta, indent=2, ensure_ascii=False))


def main():
    print("CLIENTE DE TAREAS DISTRIBUIDAS")
    print("1. Saludar")
    print("2. Sumar dos números")
    print("3. Convertir texto a mayúsculas")

    opcion = input("Elegí una opción: ").strip()

    if opcion == "1":
        nombre = input("Ingresá tu nombre: ").strip() or "usuario"
        tarea = {"accion": "saludar", "datos": {"nombre": nombre}}
    elif opcion == "2":
        try:
            a = float(input("Primer número: "))
            b = float(input("Segundo número: "))
        except ValueError:
            print("Error: ingresá números válidos.")
            return
        tarea = {"accion": "sumar", "datos": {"a": a, "b": b}}
    elif opcion == "3":
        texto = input("Ingresá un texto: ")
        tarea = {"accion": "mayusculas", "datos": {"texto": texto}}
    else:
        print("Opción no válida.")
        return

    try:
        enviar_tarea(tarea)
    except (ConnectionRefusedError, TimeoutError, socket.timeout):
        print("No se pudo conectar con el servidor. Verificá que esté ejecutándose.")
    except OSError as error:
        print(f"Error de comunicación: {error}")


if __name__ == "__main__":
    main()
