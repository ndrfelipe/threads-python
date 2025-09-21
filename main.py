# main.py (Versão Final com Controle de Volume)

import threading
import time
import pygame
import os
from Instrumento import Instrumento

def metronomo(condicao, bpm_info, lock_bpm, parar_evento):
    print(f"Metrônomo iniciado com BPM: {bpm_info['value']}")
    while not parar_evento.is_set():
        with lock_bpm:
            intervalo = 60 / bpm_info['value']
        
        if parar_evento.wait(timeout=intervalo):
            break

        with condicao:
            condicao.notify_all()
    
    print("Metrônomo parado.")

def main():
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=8, buffer=512)
    
    master_bpm = {'value': 120}
    bpm_lock = threading.Lock()
    condicao_metronomo = threading.Condition()
    parar_threads = threading.Event()
    
    # NOVO: Evento para sinalizar que a primeira faixa foi tocada e todas devem começar a tocar em background.
    playback_inicio_global = threading.Event()

    faixas = {
        "bass": "music/[bass]-sobrevivendo-no-inferno-Jorge.mp3",
        "drums": "music/[drums]-sobrevivendo-no-inferno-Jorge.mp3",
        "music": "music/[music]-sobrevivendo-no-inferno-Jorge.mp3",
        "vocals": "music/[vocals]-sobrevivendo-no-inferno-Jorge.mp3"
    }

    for nome, path in faixas.items():
        if not os.path.exists(path):
            print(f"\nAVISO: Arquivo de áudio não encontrado em '{path}' para o instrumento '{nome}'.\n")
            return

    instrumentos = {
        nome: Instrumento(nome.capitalize(), arquivo, condicao_metronomo, playback_inicio_global)
        for nome, arquivo in faixas.items()
    }
    
    thread_metronomo = threading.Thread(target=metronomo, args=(condicao_metronomo, master_bpm, bpm_lock, parar_threads))
    thread_metronomo.start()

    for instrumento in instrumentos.values():
        instrumento.start()

    print("\n--- Mesa de DJ Profissional ---\n")
    print("Comandos disponíveis:")
    print("  - play <instrumento> | all")
    print("  - pausar <instrumento> | all")
    print("  - bpm <novo_bpm>")
    print("  - status")
    print("  - sair")

    try:
        while not parar_threads.is_set():
            comando = input("\n> ").strip().lower().split()
            if not comando: continue

            acao = comando[0]

            if acao == "sair":
                print("Sinal de encerramento enviado a todas as threads...")
                parar_threads.set() # Sinaliza para o metrônomo parar

                # --- CORREÇÃO CRÍTICA ADICIONADA AQUI ---
                # Sinaliza para CADA instrumento parar individualmente
                for inst in instrumentos.values():
                    inst.parar()
                # -----------------------------------------

                # Notifica uma última vez para destravar qualquer thread que esteja em wait()
                with condicao_metronomo:
                    condicao_metronomo.notify_all()
                
                break

            elif acao == "play" and len(comando) > 1:
                # NOVO: Se for o primeiro play, aciona o evento de início global
                if not playback_inicio_global.is_set():
                    print("Iniciando playback global na próxima batida...")
                    playback_inicio_global.set()

                nome_inst = comando[1]
                if nome_inst == "all":
                    for inst in instrumentos.values():
                        inst.play()
                elif nome_inst in instrumentos:
                    instrumentos[nome_inst].play()
                else:
                    print(f"Instrumento '{nome_inst}' não encontrado.")
            
            elif acao == "pausar" and len(comando) > 1:
                nome_inst = comando[1]
                if nome_inst == "all":
                    for inst in instrumentos.values():
                        inst.pausar()
                elif nome_inst in instrumentos:
                    instrumentos[nome_inst].pausar()
                else:
                    print(f"Instrumento '{nome_inst}' não encontrado.")
            
            elif acao == "bpm" and len(comando) > 1:
                try:
                    novo_bpm = int(comando[1])
                    if novo_bpm > 0:
                        with bpm_lock:
                            master_bpm['value'] = novo_bpm
                        print(f"Master BPM alterado para {novo_bpm}.")
                    else:
                        print("O BPM deve ser um número positivo.")
                except ValueError:
                    print("BPM inválido. Por favor, insira um número inteiro.")

            elif acao == "status":
                print("\n--- Status das Faixas ---")
                with bpm_lock:
                    print(f"Master BPM: {master_bpm['value']}")
                for nome, inst in instrumentos.items():
                    estado = "Tocando" if inst.pausado.is_set() else "Pausado"
                    print(f"- {inst.nome}: {estado}")
            
            else:
                print("Comando inválido.")
    except KeyboardInterrupt:
        print("\nInterrupção detectada, encerrando...")
        parar_threads.set()
        with condicao_metronomo:
            condicao_metronomo.notify_all()

    print("Encerrando... Aguardando threads finalizarem.")
    
    # --- LÓGICA DE ENCERRAMENTO CORRIGIDA ---
    # 1. Para todos os sons que o Pygame está tocando
    pygame.mixer.stop()

    # 2. Aguarda as threads encerrarem
    thread_metronomo.join()
    for instrumento in instrumentos.values():
        instrumento.join()

    # 3. Encerra o Pygame
    pygame.quit()
    print("Mesa de DJ encerrada com sucesso.")

if __name__ == "__main__":
    main()