import asyncio
import json
from collections import deque
import uuid

workers = {}  
pending_tasks = deque() 
task_to_client = {} 

async def handle_connection(reader, writer):
    """
    Gestiona cada nueva conexión, identificando si es un cliente o un worker.
    """
    peername = writer.get_extra_info('peername')
    print(f"Nueva conexión desde {peername}")

    try:
        data = await reader.read(4096)
        message = json.loads(data.decode())

        if message.get("type") == "register" and message.get("role") == "worker":
            worker_id = message["id"]
            workers[worker_id] = (reader, writer)
            print(f"Worker '{worker_id}' registrado. Total de workers: {len(workers)}")
            await handle_worker(worker_id, reader, writer)
        
        elif message.get("type") == "task":
            await handle_client_task(message, writer)
            while True:
                data = await reader.read(4096)
                if not data:
                    break
                message = json.loads(data.decode())
                await handle_client_task(message, writer)
        
        else:
            print("Conexión no identificada. Cerrando.")

    except (asyncio.IncompleteReadError, ConnectionResetError):
        print(f"Conexión con {peername} perdida inesperadamente.")
    except Exception as e:
        print(f"Error gestionando conexión con {peername}: {e}")
    finally:
        
        disconnected_worker = [wid for wid, (r, w) in workers.items() if w == writer]
        if disconnected_worker:
            wid = disconnected_worker[0]
            del workers[wid]
            print(f"Worker '{wid}' desconectado. Workers restantes: {len(workers)}")
        
        writer.close()
        await writer.wait_closed()
        print(f"Conexión con {peername} cerrada.")

async def handle_client_task(task_message, client_writer):
    """
    Añade una nueva tarea de un cliente a la cola de pendientes.
    """
    task_id = str(uuid.uuid4())
    payload = task_message["payload"]
    pending_tasks.append((task_id, payload, client_writer))
    task_to_client[task_id] = client_writer
    print(f"Nueva tarea '{payload}' (ID: {task_id}) añadida a la cola. Tareas pendientes: {len(pending_tasks)}")
    
    ack_message = {"type": "ack", "task_id": task_id, "status": "recibida"}
    client_writer.write(json.dumps(ack_message).encode())
    await client_writer.drain()

async def handle_worker(worker_id, worker_reader, worker_writer):
    """
    Bucle para recibir resultados de un worker específico.
    """
    while True:
        data = await worker_reader.read(4096)
        if not data:
            break 
        
        result_message = json.loads(data.decode())
        if result_message.get("type") == "result":
            task_id = result_message["task_id"]
            client_writer = task_to_client.get(task_id)
            if client_writer and not client_writer.is_closing():
                print(f"Enviando resultado de la tarea {task_id} al cliente.")
                client_writer.write(json.dumps(result_message).encode())
                await client_writer.drain()
                del task_to_client[task_id]
            else:
                print(f"El cliente para la tarea {task_id} ya no está conectado. Resultado descartado.")
            
            workers[worker_id] = (worker_reader, worker_writer)

async def dispatcher():
    """
    Bucle principal que toma tareas de la cola y las envía a workers disponibles.
    """
    print("Dispatcher iniciado. Esperando tareas y workers...")
    while True:
        if pending_tasks and workers:
            available_worker_id = next(iter(workers), None)

            if available_worker_id:
                worker_reader, worker_writer = workers.pop(available_worker_id) 
                
                task_id, payload, client_writer = pending_tasks.popleft()
                
                print(f"Asignando tarea '{payload}' (ID: {task_id}) a {available_worker_id}")
                
                task_to_send = {"task_id": task_id, "payload": payload}
                worker_writer.write(json.dumps(task_to_send).encode())
                await worker_writer.drain()
                
                workers[available_worker_id] = (worker_reader, worker_writer)

        await asyncio.sleep(0.1) 

async def main():
    server = await asyncio.start_server(handle_connection, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print(f'Servidor escuchando en {addr}')

    dispatcher_task = asyncio.create_task(dispatcher())

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor apagando.")