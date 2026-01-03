#   Docker container for the `obs-shards` backend
FROM python:3.12-slim

# Variáveis de ambiente básicas
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho dentro do container
WORKDIR /app

# Dependências de sistema mínimas (Postgres-ready)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas requirements primeiro (cache eficiente)
COPY requirements.txt .

# Instala dependências Python
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copia o restante do código
COPY . .

# Porta padrão do Django
EXPOSE 8000

# Comando padrão (dev)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
