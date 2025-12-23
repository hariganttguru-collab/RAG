@echo off
cd /d "%~dp0"
python -m daphne -b 127.0.0.1 -p 8000 config.asgi:application

