#!/bin/sh
set -e

# Aguardando PostgreSQL
echo "⏳ Aguardando PostgreSQL em $DB_HOST:$DB_PORT..."
until nc -z $DB_HOST $DB_PORT; do
  sleep 2
done
echo "✅ PostgreSQL está pronto!"

# Rodando migrations automaticamente
echo "🚀 Rodando migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Rodando servidor Django
echo "🚀 Subindo servidor Django..."
python manage.py runserver 0.0.0.0:8000
