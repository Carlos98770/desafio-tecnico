# Usa imagem base do Python
FROM python:3.13.3

# Diretório de trabalho dentro do container
WORKDIR /app

# Dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    pkg-config \
    netcat-openbsd \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala Poetry dentro do container
RUN curl -sSL https://install.python-poetry.org | python3 -

# Adiciona Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

# Copia arquivos de dependência para cache eficiente
COPY pyproject.toml poetry.lock* ./

# Configura o Poetry para não criar venv dentro do container
ENV POETRY_VIRTUALENVS_CREATE=false \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instala dependências do projeto
RUN poetry install --no-root --no-interaction --no-ansi

# Copia todo o código do projeto para dentro do container
COPY . .

# Copia e dá permissão ao script de inicialização
COPY script.sh .
RUN chmod +x script.sh

# Expõe a porta padrão do Django
EXPOSE 8000

# Comando de inicialização
CMD ["sh", "script.sh"]
