# Programación sobre Redes - Tecnicatura en Desarrollo de Software (IFTS N° 29)

## Descripción del Repositorio

Este repositorio contiene las soluciones a las Prácticas Formativas Obligatorias (PFO) y otros ejercicios realizados durante la cursada de la materia "Programación sobre Redes" en el segundo cuatrimestre de 2025 del terecer año de la tecnicatura.

El objetivo de este espacio es documentar el progreso práctico en la materia, demostrando la aplicación de conceptos clave como concurrencia, `sockets`, arquitecturas cliente-servidor, y protocolos de alto nivel como HTTP.

**Profesor:** Alan Portillo, Germán Ríos

---

## Contenido del Repositorio

El repositorio está estructurado por entregas, cada una representando un hito en el aprendizaje de la materia.

### 📂 `Actividad-ConcurrenciaConHilos/`
- **Descripción:** Ejercicios introductorios a la programación concurrente en Python, utilizando el módulo `threading` para ejecutar tareas en paralelo simulado y coordinar su finalización.
- **Conceptos Aplicados:**
  - Creación y gestión de `threading.Thread`.
  - Sincronización con `thread.join()` y `threading.Condition`.

### 📂 `PFO1-Próximamente/`
- **Descripción:** Implementación de un sistema de chat cliente-servidor `multi-threaded`, capaz de gestionar múltiples clientes de forma concurrente. Los mensajes se persisten de forma segura (`thread-safe`) en una base de datos SQLite.
- **Conceptos Aplicados:**
  - Programación de `sockets` TCP/IP.
  - Modelo concurrente de un hilo por cliente.
  - Sincronización de acceso a recursos compartidos con `threading.Lock`.
  - Persistencia de datos con `sqlite3`.

### 📂 `PFO2-API_REST_con_Flask/`
- **Descripción:** Desarrollo de una API RESTful utilizando Flask para la gestión de usuarios, incluyendo registro y autenticación. Se implementó un cliente de consola para interactuar con los `endpoints`.
- **Conceptos a Aplicar:**
  - Modelo Cliente-Servidor sobre el protocolo HTTP.
  - Diseño de `endpoints` RESTful (`POST`, `GET`).
  - Seguridad de contraseñas mediante `hashing` (Werkzeug).
  - Consumo de APIs con la librería `requests`.

### 📂 `PFO3-Próximamente`
- **Descripción:** Simulación de una arquitectura de sistema distribuido (Dispatcher-Worker) para el procesamiento asíncrono de tareas. La implementación utiliza `sockets` y el módulo `asyncio` para un manejo de I/O no bloqueante y de alto rendimiento.
- **Conceptos a Aplicar:**
  - Programación de `sockets` asíncronos con `asyncio`.
  - Patrones de arquitectura distribuida.
  - Diseño de un protocolo de comunicación basado en JSON.
  - Gestión de un `pool` de `workers` y distribución de tareas.

---

## Stack Tecnológico Principal

- **Lenguaje:** Python 3.13.7
- **Librerías Principales:**
  - **Concurrencia:** `threading`, `asyncio`
  - **Networking:** `socket`
  - **Web:** `Flask`, `Werkzeug`
  - **Cliente HTTP:** `requests`
  - **Base de Datos:** `sqlite3`
- **Entorno de Desarrollo:** Visual Studio Code

---

## Cómo Ejecutar los Proyectos

Cada carpeta de práctica (`Actividad-....`, `PFO1-....`, etc.) contiene su propio `README.md` con instrucciones detalladas, diagramas de arquitectura y evidencia de las pruebas realizadas para la configuración y ejecución de los scripts correspondientes.