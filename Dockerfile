FROM ubuntu:22.04

# Instala dependências
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Instala Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Puxa modelo pequeno
RUN ollama pull llama3.2:1b

# Instala Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copia app
COPY app.py .

# Expõe porta
EXPOSE 8080

# Inicia apenas o Flask (Ollama inicia via thread)
CMD ["python3", "app.py"]
