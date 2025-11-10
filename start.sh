#!/bin/bash
# Inicia Ollama em segundo plano
ollama serve &

# Aguarda Ollama inicializar
sleep 10

# Inicia Flask na porta 8080
python3 app.py
