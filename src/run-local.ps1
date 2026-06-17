# Ejecutar la API en local (PowerShell)
# Uso: .\run-local.ps1

$ErrorActionPreference = "Stop"

$PythonCandidates = @(
    "C:\Users\kdraf\AppData\Local\Programs\Python\Python311\python.exe",
    "C:\Users\kdraf\AppData\Local\Programs\Python\Python312\python.exe"
)

$Python = $PythonCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $Python) {
    Write-Host "Python no encontrado. Instala Python 3.11 desde https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "Marca la opcion 'Add Python to PATH' durante la instalacion." -ForegroundColor Yellow
    exit 1
}

$env:STORAGE_MODE = "local"
$env:FLASK_DEBUG = "1"

Write-Host "Usando: $Python" -ForegroundColor Cyan
Write-Host "Portal: http://localhost:5000/portal" -ForegroundColor Green

& $Python -m pip install -r requirements.txt
& $Python app.py
