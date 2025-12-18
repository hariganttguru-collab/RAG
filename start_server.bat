@echo off
echo Starting Project Management Learning Portal Server...
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if .env file exists
if not exist ".env" (
    echo Warning: .env file not found. Please create it with your OPENAI_API_KEY.
    echo.
)

REM Start Daphne server
echo Starting Daphne server on http://127.0.0.1:8000
echo Press Ctrl+C to stop the server
echo.

python -m daphne -b 127.0.0.1 -p 8000 config.asgi:application

pause

