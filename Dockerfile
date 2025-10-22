FROM python:3.13.3

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    pkg-config \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY . .

COPY script.sh .
RUN chmod +x script.sh

CMD ["sh", "script.sh"]
