import threading

condicion = threading.Condition()

resultados = {}

def sumar_numeros(nombre):
    suma = sum(range(1,6))
    with condicion:
        resultados[nombre] = suma
        print(f"{nombre} termino de sumar.")
        condicion.notify_all()

hilo1 = threading.Thread(target=sumar_numeros, args=("Hilo 1",))
hilo2 = threading.Thread(target=sumar_numeros, args=("Hilo 2",))

print("Iniciando hilos...")
hilo1.start()
hilo2.start()

with condicion:
    while len(resultados) < 2:
        condicion.wait()
print(f"Resultados finales (recopilados por el hilo principal): {resultados}")
print("Programa Finalizado.")

hilo1.join()
hilo2.join()