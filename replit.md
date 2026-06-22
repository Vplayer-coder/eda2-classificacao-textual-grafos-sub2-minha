# Classificador Semântico de Reviews via Grafos Ponderados

An academic Python tool for automated semantic classification of Steam game reviews (Subnautica 2) using a custom Weighted Graph and BFS (Breadth-First Search) algorithm.

## Project Overview

Classifies player feedback into three profiles:
1. **Casual / Imersivo** — Exploration, narrative, co-op
2. **Técnico / Performance** — Optimization, bugs, hardware
3. **Hardcore / Sobrevivência** — Combat, resource scarcity, difficulty

## Running the Project

**Main classifier (generates full statistical report):**
```bash
python classificador_bfs.py
```

**Interactive XAI audit tool (step-by-step BFS trace):**
```bash
python auditoria_grafo.py
```

## Key Files

- `classificador_bfs.py` — Main entry point; builds graph, trains weights, processes all reviews
- `auditoria_grafo.py` — Interactive explainability tool for manual review testing
- `estrutura_dados.py` — Custom FIFO Queue and base Graph implementations
- `extrator_dados_steam.py` — Steam API data ingestion and text preprocessing
- `reviews_subnautica2.json` — Dataset with ~2,700 cleaned and tokenized reviews

## Technical Notes

- Pure Python 3.x — no external libraries (academic constraint)
- Graph implemented via parallel arrays (no dicts/hashmaps)
- BFS-based Spreading Activation for multi-label classification
- 30% statistical threshold for multi-label assignment

## User Preferences

(none yet)
