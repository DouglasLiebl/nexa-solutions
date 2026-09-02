#!/bin/sh
set -e

echo "Aguardando PostgreSQL em ${POSTGRES_HOST:-db}:${POSTGRES_PORT:-5432}..."

until python - <<'PY'
import os
import sys

import psycopg2

required = ("POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST")
missing = [name for name in required if not os.environ.get(name)]
if missing:
    print(f"Variáveis de ambiente obrigatórias ausentes: {', '.join(missing)}", file=sys.stderr)
    sys.exit(1)

try:
    psycopg2.connect(
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["POSTGRES_HOST"],
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
