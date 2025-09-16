from Instrumento import *

def main():

    # threads para cada instrumento
    instrumentos = {
        "bateria": Instrumento("Bateria", bpm=120),
        "baixo": Instrumento("Baixo", bpm=100),
        "synth": Instrumento("Synth", bpm=140),
    }

    # iniciando todas as threads
    for instrumento in instrumentos.values():
        instrumento.start()

    print("\n--- Mesa de DJ ---\n")
    print("Comandos disponíveis:")
    print("  - play <instrumento>")
    print("  - pausar <instrumento>")
    print("  - bpm <instrumento> <novo_bpm>")
    print("  - status")
    print("  - sair")

    while True:
        comando = input("\n> ").strip().split()
        if not comando:
            continue

        acao = comando[0]

        if acao == "sair":
            for instrumento in instrumentos.values():
                instrumento.parar()
            break

        elif acao == "pausar" and len(comando) > 1:
            nome_inst = comando[1]
            if nome_inst in instrumentos:
                instrumentos[nome_inst].pausar()
            else:
                print(f"Instrumento '{nome_inst}' não encontrado.")
        
        elif acao == "play" and len(comando) > 1:
            nome_inst = comando[1]
            if nome_inst in instrumentos:
                instrumentos[nome_inst].play()
            else:
                print(f"Instrumento '{nome_inst}' não encontrado.")
        
        elif acao == "bpm" and len(comando) > 2:
            nome_inst = comando[1]
            try:
                novo_bpm = int(comando[2])
                if nome_inst in instrumentos:
                    instrumentos[nome_inst].mudar_bpm(novo_bpm)
                else:
                    print(f"Instrumento '{nome_inst}' não encontrado.")
            except ValueError:
                print("BPM inválido. Por favor, insira um número inteiro.")

        elif acao == "status":
            print("\n--- Status das Faixas ---")
            for nome, inst in instrumentos.items():
                estado = "Pausado" if not inst.pausado.is_set() else "Tocando"
                print(f"- {nome.capitalize()}: {estado} (BPM: {inst.bpm})")
        
        else:
            print("Comando inválido. Tente novamente.")
        
    # Aguarda todas as threads encerrarem
    for instrumento in instrumentos.values():
        instrumento.join()

        print("Mesa de DJ encerrada com sucesso.")

if __name__ == "__main__":
    main()
