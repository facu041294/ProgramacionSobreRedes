import asyncio
import json
import time
import random

async def worker_client(worker_id):
    """
    Simula un worker que se conecta al servidor, se registra y procesa tareas.
    """
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
        print(f"[Worker {worker_id}] Conectado al servidor.")

        registration_message = {"type": "register", "role": "worker", "id": worker_id}
        writer.write(json.dumps(registration_message).encode())
        await writer.drain()
        print(f"[Worker {worker_id}] Registrado en el servidor.")

        while True:
            data = await reader.read(4096)
            if not data:
                print(f"[Worker {worker_id}] Conexión cerrada por el servidor.")
                break

            task = json.loads(data.decode())
            print(f"[Worker {worker_id}] Recibida tarea: {task['payload']}")
            
            processing_time = random.uniform(2, 5)
            await asyncio.sleep(processing_time)
            
            result = f"Tarea '{task['payload']}' completada por {worker_id} en {processing_time:.2f} segundos."
            
            result_message = {"type": "result", "task_id": task["task_id"], "result": result}
            writer.write(json.dumps(result_message).encode())
            await writer.drain()
            print(f"[Worker {worker_id}] Resultado enviado.")

    except ConnectionRefusedError:
        print(f"[Worker {worker_id}] No se pudo conectar al servidor. ¿Está corriendo?")
    except Exception as e:
        print(f"Error en Worker {worker_id}: {e}")
    finally:
        if 'writer' in locals():
            writer.close()
            await writer.wait_closed()
        print(f"[Worker {worker_id}] Desconectado.")

if __name__ == "__main__":
    worker_id = f"Worker-{random.randint(100, 999)}"
    try:
        asyncio.run(worker_client(worker_id))
    except KeyboardInterrupt:
        print(f"\n[Worker {worker_id}] Apagando.")