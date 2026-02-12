#!/bin/bash
# Azure Web App startup – run from app root (where manage.py and config/ live)
set -e
cd /home/site/wwwroot
# If project is in RAG subfolder (nested deploy), use it
if [ -f RAG/manage.py ]; then
  cd RAG
fi
export DJANGO_SETTINGS_MODULE=config.settings
python manage.py collectstatic --noinput --no-color 2>/dev/null || true
PORT="${PORT:-8000}"
exec gunicorn --bind=0.0.0.0:$PORT --timeout 600 --workers 2 config.wsgi:application
