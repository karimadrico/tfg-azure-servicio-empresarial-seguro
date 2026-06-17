#!/usr/bin/env bash
# Ejecutar la API en local (Git Bash en Windows)

PYTHON="/c/Users/kdraf/AppData/Local/Programs/Python/Python311/python.exe"

if [ ! -f "$PYTHON" ]; then
  echo "No se encontró Python 3.11 en la ruta esperada."
  echo "Instálalo desde https://www.python.org/downloads/"
  exit 1
fi

export STORAGE_MODE=local
export FLASK_DEBUG=1

"$PYTHON" -m pip install -r requirements.txt
"$PYTHON" app.py
