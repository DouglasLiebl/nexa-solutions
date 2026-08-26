#!/bin/sh
set -e

echo "Aguardando PostgreSQL em ${POSTGRES_HOST:-db}:${POSTGRES_PORT:-5432}..."

until python - <<'PY'
import os
import sys

import psycopg2

try:
    psycopg2.connect(
        dbname=os.environ.get("POSTGRES_DB", "nexa_chamados"),
        user=os.environ.get("POSTGRES_USER", "nexa_user"),
        password=os.environ.get("POSTGRES_PASSWORD", ""),
        host=os.environ.get("POSTGRES_HOST", "db"),
        port=os.environ.get("POSTGRES_PORT", "5432"),
        connect_timeout=3,
    ).close()
except Exception:
    sys.exit(1)
PY
do
  sleep 1
done

echo "PostgreSQL disponível. Aplicando migrações..."
python manage.py migrate --noinput

exec "$@"
