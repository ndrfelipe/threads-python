# Mesa de DJ com Threads em Python

Um simulador de mesa de DJ multicanal em **Python**, que utiliza **threads** para sincronizar múltiplas faixas `.mp3` em tempo real. Demonstra conceitos de programação concorrente aplicados ao controle de playback via CLI.

---
# Índice

1. [Funcionalidades](#-funcionalidades)  
2. [Estrutura do Projeto](#-estrutura-do-projeto)  
3. [Requisitos](#-requisitos)  
4. [Como Executar](#-como-executar)  
5. [Comandos](#-comandos-disponíveis)
6. [Como funciona](#-como-funciona)
7. [Observações](#-observações)
8. [O que é Thread](#-o-que-é-thread)  
9. [O que é Multithreading](#-o-que-é-multithreading)  
10. [Como o Projeto Utiliza Threads](#-como-o-projeto-utiliza-threads)
11. [Authors](#-authors)  
---

  ## Funcionalidades
- Playback sincronizado de múltiplas faixas `.mp3/.wav`.  
- Controle em tempo real via CLI.  
- Play / Pause individual e global.  
- Pause inteligente: a faixa retorna no ponto exato sem perder sincronia.  
- Ajuste dinâmico de BPM (batidas por minuto).  
- Visualização do status (BPM e estado das faixas).



---

## Estrutura do projeto
```text
mesa-dj-python/
├── music/           # faixas .mp3 (vocals.mp3, drums.mp3, bass.mp3, etc.)
├── Instrumento.py   # classe Instrumento (cada instância roda em sua própria thread)
├── main.py          # interface CLI, metrônomo e inicialização
└── README.md
```

## Requisitos
- Python 3.x
- pip
- Biblioteca: pygame
```text
pip install pygame
```

## Como executar
```text
python main.py
```

## Comandos (CLI)
| Comando                | Descrição                                                 |
| ---------------------- | --------------------------------------------------------- |
| `play <instrumento>`   | Toca a faixa especificada. Ex: `play vocals`              |
| `play all`             | Toca todas as faixas simultaneamente                      |
| `pausar <instrumento>` | Pausa (silencia) a faixa especificada. Ex: `pausar drums` |
| `pausar all`           | Pausa (silencia) todas as faixas                          |
| `bpm <valor>`          | Ajusta o BPM. Ex: `bpm 140`                               |
| `status`               | Exibe BPM atual e estado de cada faixa                    |
| `sair`                 | Encerra o programa de forma segura                        |

## Como funciona (resumo técnico)
- Multithreading: uma thread para o CLI, uma para o metrônomo e uma por instrumento.
- Sincronização: o metrônomo usa threading.Condition para notify_all() a cada batida; as threads dos instrumentos wait() pelo sinal, garantindo execução síncrona.
- Pause inteligente: todas as faixas são reproduzidas em loop com volume 0; play ajusta o volume para 100% e pausar retorna a 0, preservando o cursor de reprodução e a sincronia.

## Observações
- Todas as faixas devem ter a mesma duração para manter a sincronia.

---

## O que é Thread
Uma **thread** é a menor unidade de execução que um processo pode ter.  
Ela permite que partes diferentes de um mesmo programa sejam executadas **simultaneamente**, sem precisar esperar que uma parte termine para outra começar.  

Em termos simples:
- Um **programa** é um processo.  
- Uma **thread** é como um "fluxo de execução" dentro desse processo.  

---

## O que é Multithreading
**Multithreading** é a técnica de executar várias threads em paralelo dentro do mesmo programa.  

Vantagens:
- Melhor aproveitamento dos recursos do processador.  
- Execução concorrente de tarefas (ex: tocar música e, ao mesmo tempo, responder comandos do usuário).  
- Maior responsividade em aplicações interativas.  

---

## Como o Projeto Utiliza Threads
Neste projeto, o multithreading é essencial para manter a sincronia entre as faixas musicais e, ao mesmo tempo, processar comandos do usuário em tempo real.

- **Thread principal**  
  Responsável pela interface de linha de comando (CLI). Recebe os comandos `play`, `pausar`, `bpm`, `status`, etc.  

- **Thread do Metrônomo**  
  Atua como o "maestro". A cada batida (definida pelo BPM), envia um sinal (`notify_all`) para sincronizar todas as faixas.  

- **Threads de Instrumentos** (`Instrumento.py`)  
  Cada instrumento (bateria, baixo, vocais, etc.) roda em sua própria thread.  
  - Inicia em loop infinito, mas em **mudo** (volume 0).  
  - Quando o usuário executa `play <instrumento>`, o volume sobe para 100%.  
  - Quando executa `pausar <instrumento>`, o volume volta a 0.  
  - Isso garante que todas as faixas continuem **alinhadas no tempo**, mesmo quando pausadas.  

Esse modelo só é possível porque cada faixa roda em **threads independentes**, mas sincronizadas pelo **metrônomo**.

---

## Authors
- André F. S. Braga - ndrfelipe (git)
- Letícia G. C. Silva - Letícia.Gabs (git)
- Manuele Macêdo P. da Silva - manuelemacedo (git)
- Dayvid Cristiano V. da Silva - dayvidcristiano (git)
- Jeniffer Cristine Lopes da Conceição - jenixcri (git)
