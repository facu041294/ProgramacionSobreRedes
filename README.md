# Programación sobre Redes - Tecnicatura en Desarrollo de Software (IFTS N° 29)

## Descripción del Repositorio

Este repositorio contiene las soluciones a las Prácticas Formativas Obligatorias (PFO) y otros ejercicios realizados durante la cursada de la materia "Programación sobre Redes" en el segundo cuatrimestre de 2025 del terecer año de la tecnicatura.

El objetivo de este espacio es documentar el progreso práctico en la materia, aplicando los conceptos teóricos de concurrencia, paralelismo, comunicación entre procesos y arquitecturas de red en Python.

**Profesor:** Alan Portillo, Germán Ríos

---

## Contenido del Repositorio

### 📂 `PFO1-ConcurrenciaConHilos/`
- **Descripción:** Solución a la primera Práctica Formativa Obligatoria, enfocada en los fundamentos de la programación concurrente utilizando el módulo `threading` de Python.
- **Archivos Clave:**
  - `ContandoEnParalelo.py`: Implementación de dos hilos que ejecutan una tarea de conteo de forma concurrente.
  - `SincronizacionDeHilos.py`: Solución al problema de sincronización utilizando `threading.Condition` para coordinar la finalización de dos hilos antes de procesar sus resultados.
- **Conceptos Aplicados:**
  - Creación y gestión de `threads`.
  - El problema del `Global Interpreter Lock (GIL)`.
  - Sincronización de hilos con `join()` y `Condition variables`.
  - Prevención de `race conditions`.

### 📂 `PFO2-API_REST_con_Flask/`
- **Descripción:** (Próximamente) Desarrollo de una API RESTful simple utilizando Flask y SQLite, con un cliente de consola para interactuar con ella.
- **Conceptos a Aplicar:**
  - Modelo Cliente-Servidor.
  - Protocolo HTTP (endpoints, métodos).
  - Autenticación básica y `hashing` de contraseñas.
  - Persistencia de datos con SQLite.

### 📂 `PFO3-Próximamente`
- **Descripción:** (Próximamente)
- **Conceptos a Aplicar:**
  - Próximamente.
---

## Stack Tecnológico Principal

- **Lenguaje:** Python 3.13
- **Librerías Principales:**
  - `threading`
  - `socket` (próximamente)
  - `Flask` (próximamente)
- **Entorno de Desarrollo:** Visual Studio Code

---

## Cómo Ejecutar los Proyectos

Cada carpeta de práctica contiene su propio `README.md` con instrucciones detalladas para la configuración y ejecución de los scripts correspondientes.