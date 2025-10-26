import asyncio
import json
import uuid

async def send_task(writer, task_payload):
    """
    Envía una única tarea al servidor.
    """
    task_message = {"type": "task", "payload": task_payload}
    writer.write(json.dumps(task_message).encode())
    await writer.drain()
    print(f"-> Tarea enviada: '{task_payload}'")

async def client():
    """
    Cliente principal que se conecta, envía tareas y escucha resultados.
    """
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
        print("Conectado al servidor.")

        tasks_to_send = ["Renderizar escena", "Compilar shader", "Hornear texturas", "Ejecutar simulación física"]
        sender_task = asyncio.create_task(send_tasks_periodically(writer, tasks_to_send))

        async for data in reader:
            message = json.loads(data.decode())
            if message.get("type") == "ack":
                print(f"<- ACK recibido del servidor para la tarea ID: {message['task_id']}")
            elif message.get("type") == "result":
                print(f"<- Resultado final recibido: {message['result']}")

        sender_task.cancel()
        print("Conexión cerrada por el servidor.")

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor.")
    finally:
        if 'writer' in locals() and not writer.is_closing():
            writer.close()
            await writer.wait_closed()
        print("Cliente desconectado.")

async def send_tasks_periodically(writer, tasks):
    for task in tasks:
        await send_task(writer, task)
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(client())
    except KeyboardInterrupt:
        print("\nCliente apagando.")