# PFO 1: Concurrencia con Hilos en Python

## Descripción

Esta carpeta contiene la solución a la **Primera Práctica Formativa Obligatoria** de la materia "Programación sobre Redes". El objetivo de esta práctica es demostrar la comprensión y aplicación de los conceptos fundamentales de la programación concurrente en Python utilizando el módulo `threading`.

Se resuelven dos problemas específicos:
1.  **Conteo Concurrente:** La creación de dos hilos que ejecutan una tarea de conteo en paralelo simulado.
2.  **Sincronización de Hilos:** La coordinación de dos hilos para que un resultado final solo se procese después de que ambos hayan completado sus cálculos, utilizando una `threading.Condition` para una sincronización robusta.

---

## Contenido

-   `ContandoEnParalelo.py`: Script que resuelve el Problema 1.
-   `SincronizacionDeHilos.py`: Script que resuelve el Problema 2.

---

## Requisitos

-   Python 3.x

No se requieren librerías externas más allá de las incluidas en la biblioteca estándar de Python.

---

## Cómo Ejecutar los Scripts

Para ejecutar las soluciones, navega a esta carpeta (`PFO1-ConcurrenciaConHilos/`) en tu terminal y utiliza los siguientes comandos:

**1. Para ejecutar el Problema 1 (Conteo en Paralelo):**
```bash
python ContandoEnParalelo.py
```
**Salida Esperada:**
Verás los mensajes "Hilo 1 terminó de sumar" y "Hilo 2 terminó de sumar". Inmediatamente después, el hilo principal imprimirá una única vez los "Resultados finales" conteniendo la suma de ambos hilos, seguido del mensaje "Programa finalizado.". Esto demuestra que la sincronización con threading.Condition funcionó correctamente.

---

### **Conceptos Clave Implementados**
- Creación y lanzamiento de hilos con threading.Thread.
- Uso de thread.join() para esperar la finalización de un hilo.
- Gestión de recursos compartidos (un diccionario resultados).
- Sincronización avanzada con threading.Condition para la coordinación entre hilos.
- Uso del patrón with para la adquisición y liberación automática de locks y condiciones.
