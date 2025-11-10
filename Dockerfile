FROM ubuntu:22.04

# Instala dependências
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Instala Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Instala Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copia app
COPY app.py .

# Expõe porta do Flask
EXPOSE 8080

# Inicia ambos serviços
CMD python3 app.py & ollama serve
