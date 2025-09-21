# Instrumento.py (Versão Final com Controle de Volume)

import threading
import pygame

class Instrumento(threading.Thread):
    def __init__(self, nome, arquivo_audio, condicao_metronomo, evento_inicio_global):
        super().__init__()
        self.nome = nome
        self.condicao_metronomo = condicao_metronomo
        
        # NOVO: Evento compartilhado que sinaliza o início do playback de todas as faixas
        self.evento_inicio_global = evento_inicio_global

        self.pausado = threading.Event()
        self.pausado.clear()

        self.parar_execucao = threading.Event()
        
        try:
            self.som = pygame.mixer.Sound(arquivo_audio)
        except pygame.error as e:
            print(f"ERRO: Não foi possível carregar o arquivo de áudio {arquivo_audio}: {e}")
            self.som = None
        
        # NOVO: Controla se o loop desta faixa específica já começou
        self.loop_iniciado = False

    def run(self):
        if not self.som:
            return

        print(f"[{self.nome}] pronto.")
        
        while not self.parar_execucao.is_set():
            with self.condicao_metronomo:
                self.condicao_metronomo.wait()
            
            if self.parar_execucao.is_set():
                break

            # --- LÓGICA PRINCIPAL DE CONTROLE DE VOLUME E PLAYBACK ---

            # 1. VERIFICA SE O PLAYBACK GLOBAL DEVE COMEÇAR
            # Se o sinal global foi dado E esta faixa ainda não começou, inicia-a em loop e silenciosamente.
            if self.evento_inicio_global.is_set() and not self.loop_iniciado:
                self.som.play(loops=-1)  # Começa o loop infinito
                self.som.set_volume(0.0) # Começa com volume 0 (mudo)
                self.loop_iniciado = True
                print(f"[{self.nome}] playback em background iniciado.")

            # 2. CONTROLA O VOLUME (MUDO/NÃO MUDO)
            # Se o loop já foi iniciado, apenas ajusta o volume conforme o comando do usuário.
            if self.loop_iniciado:
                if self.pausado.is_set(): # Se o usuário deu "play" nesta faixa
                    self.som.set_volume(1.0) # Aumenta o volume para 100%
                else: # Se o usuário deu "pausar" nesta faixa
                    self.som.set_volume(0.0) # Zera o volume (silencia)

        # Ao sair do loop, garante que o som desta faixa pare.
        self.som.stop()
        print(f"[{self.nome}] Parando execução.")

    def pausar(self):
        """Define o estado desejado como 'pausado' (mudo)."""
        self.pausado.clear()
        print(f"[{self.nome}] comando 'pausar' recebido.")

    def play(self):
        """Define o estado desejado como 'play' (não mudo)."""
        self.pausado.set()
        print(f"[{self.nome}] comando 'play' recebido.")

    def parar(self):
        """Envia o sinal para a thread parar de forma segura."""
        self.parar_execucao.set()
        # O som é parado dentro do próprio loop run() ao final
        with self.condicao_metronomo:
            self.condicao_metronomo.notify()