import threading
import time

class Instrumento(threading.Thread):
    def __init__(self, nome, bpm=120):
        super().__init__()
        self.nome = nome
        self.tocando = True
        
        self.bpm = bpm
        self.intervalo = 60 / self.bpm

        self.pausado = threading.Event()
        self.pausado.set()
        self.parar_execucao = threading.Event()

    def run(self):
        print(f"{self.nome} iniciando com bpm {self.bpm}...")
        
        while not self.parar_execucao.is_set():
            self.pausado.wait() #se a thread tiver pausada, ele espera
            print(f"[{self.nome}] Tocando...")
            time.sleep(self.intervalo)
        print(f"[{self.nome}] Parando execução.")

    def pausar(self):
        self.pausado.clear()
        print(f"[{self.nome}] pausado.")

    def retomar(self):
        self.pausado.set()
        print(f"[{self.nome}] retornando.")

    def parar(self):
        self.parar_execucao.set()
        self.pausado.set()
        print(f"[{self.nome}] sinal para parar enviado.")

    def mudar_bpm(self, novo_bpm):
        self.bpm = novo_bpm
        self.intervalo = 60 / self.bpm
        print(f"[{self.nome}] BPM alterado para {self.bpm}.")

        
        
