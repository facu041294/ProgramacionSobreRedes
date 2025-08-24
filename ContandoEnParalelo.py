import threading
import time

def contar_numeros(nombre,contador):
    for i in range(1,6):
        time.sleep(1)
        print(f"{nombre} esta contando: {contador + i}")

hilo1 = threading.Thread(target=contar_numeros, args=("Hilo 1", 0))
hilo2 = threading.Thread(target=contar_numeros, args=("Hilo 2", 5))

hilo1.start()
hilo2.start()

print("Contador completo!")

hilo1.join()
hilo2.join()
