FROM ubuntu:22.04

# Instala dependências
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Instala Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Expõe porta
EXPOSE 8080

# Inicia Ollama
CMD ["ollama", "serve"]
