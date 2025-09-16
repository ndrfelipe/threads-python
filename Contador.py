import threading
import time

contador = 0

def incrementa_com_atraso():
    global contador
    for _ in range(1000):
        # Esta é a seção crítica, onde a race condition pode ocorrer.
        valor_atual = contador
        # Pequeno atraso que permite ao agendador trocar de thread.
        time.sleep(1)
        valor_novo = valor_atual + 1
        contador = valor_novo

threads = []
print("Iniciando threads para forçar a race condition...")

for i in range(1000):
    t = threading.Thread(target=incrementa_com_atraso)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Valor final do contador: {contador}")
print(f"Valor esperado: {1000 * 1000}")
print("\nCom o atraso, o valor final será quase sempre incorreto.")