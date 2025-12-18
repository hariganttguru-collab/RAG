# PowerShell script to start the Django server with WebSocket support
Write-Host "Starting Project Management Learning Portal Server..." -ForegroundColor Green
Write-Host ""

# Change to project directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "Warning: .env file not found. Please create it with your OPENAI_API_KEY." -ForegroundColor Yellow
    Write-Host ""
}

# Start Daphne server
Write-Host "Starting Daphne server on http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python -m daphne -b 127.0.0.1 -p 8000 config.asgi:application

