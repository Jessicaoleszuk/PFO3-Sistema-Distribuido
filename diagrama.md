# Diagrama de arquitectura distribuida

El siguiente diagrama representa la arquitectura propuesta. El código Python implementa los sockets TCP y el pool de hilos; Nginx, RabbitMQ, PostgreSQL y S3 se incluyen como componentes de la arquitectura objetivo y no requieren instalación para ejecutar la demostración local.

```mermaid
flowchart TD
    M[Cliente móvil] --> LB[Balanceador de carga<br/>Nginx o HAProxy]
    W[Cliente web] --> LB
    LB --> S1[Servidor de tareas 1<br/>Socket TCP]
    LB --> S2[Servidor de tareas 2<br/>Socket TCP]
    S1 --> Q[Cola de mensajes<br/>RabbitMQ]
    S2 --> Q
    Q --> WK1[Worker 1<br/>Pool de hilos]
    Q --> WK2[Worker 2<br/>Pool de hilos]
    Q --> WK3[Worker 3<br/>Pool de hilos]
    WK1 --> DB[(PostgreSQL<br/>Datos estructurados)]
    WK2 --> DB
    WK3 --> OBJ[(Almacenamiento S3<br/>Archivos y objetos)]
```

## Descripción de los componentes

- **Clientes web y móviles:** solicitan tareas al sistema.
- **Balanceador Nginx/HAProxy:** distribuye las solicitudes entre distintos servidores para evitar que toda la carga recaiga en uno solo.
- **Servidores de tareas:** reciben solicitudes y las derivan para su procesamiento.
- **Workers y pool de hilos:** ejecutan las tareas concurrentemente.
- **RabbitMQ:** permite encolar mensajes y desacoplar a los servidores de los workers.
- **PostgreSQL:** guarda información estructurada.
- **S3:** almacena archivos u objetos.

**Alcance de la implementación:** para mantener el ejercicio simple y ejecutable en una computadora, la versión entregada utiliza un servidor TCP, varios hilos para atender conexiones y un `ThreadPoolExecutor` para procesar tareas. Los componentes externos se muestran en el diagrama como una posible ampliación; no se afirma que estén conectados al código de demostración.
