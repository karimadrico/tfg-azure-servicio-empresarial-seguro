from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from functools import wraps
from typing import Any, Callable

from flask import Flask, jsonify, request

from classifier import classify_incidencia
from config import Config
from storage import IncidenciaStorage

app = Flask(__name__)
config = Config()
storage = IncidenciaStorage(config)

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
VALID_ESTADOS = {"abierta", "en_proceso", "cerrada"}
VALID_PRIORIDADES = {"baja", "media", "alta"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _next_id(incidencias: list[dict[str, Any]]) -> str:
    if not incidencias:
        return "INC-001"
    numbers = []
    for item in incidencias:
        match = re.match(r"INC-(\d+)$", item.get("id", ""))
        if match:
            numbers.append(int(match.group(1)))
    return f"INC-{max(numbers, default=0) + 1:03d}"


def _get_api_key() -> str:
    if config.API_KEY:
        return config.API_KEY

    if not config.KEY_VAULT_URL:
        return ""

    try:
        from azure.identity import DefaultAzureCredential
        from azure.keyvault.secrets import SecretClient

        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=config.KEY_VAULT_URL, credential=credential)
        secret = client.get_secret(config.KEY_VAULT_SECRET_NAME)
        return secret.value or ""
    except Exception:
        return ""


def require_auth(handler: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(handler)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        expected_key = _get_api_key()
        if not expected_key:
            return handler(*args, **kwargs)

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "No autenticado"}), 401

        provided_key = auth_header.removeprefix("Bearer ").strip()
        if provided_key != expected_key:
            return jsonify({"error": "Token inválido"}), 401

        return handler(*args, **kwargs)

    return wrapper


@app.get("/")
def root() -> Any:
    return jsonify(
        {
            "mensaje": "API TFG Servicio Empresarial Seguro",
            "version": "1.0",
            "estado": "operacional",
            "timestamp": _utc_now(),
        }
    )


@app.get("/health")
def health() -> Any:
    return jsonify(
        {
            "estado": "ok",
            "storage_mode": config.STORAGE_MODE,
            "timestamp": _utc_now(),
        }
    )


@app.get("/incidencias")
@require_auth
def list_incidencias() -> Any:
    estado = request.args.get("estado")
    prioridad = request.args.get("prioridad")
    limit = request.args.get("limit", default=50, type=int)
    offset = request.args.get("offset", default=0, type=int)

    if estado and estado not in VALID_ESTADOS:
        return jsonify({"error": "Estado inválido"}), 400
    if prioridad and prioridad not in VALID_PRIORIDADES:
        return jsonify({"error": "Prioridad inválida"}), 400
    if limit < 1 or limit > 100 or offset < 0:
        return jsonify({"error": "Parámetros de paginación inválidos"}), 400

    incidencias = storage.load()
    if estado:
        incidencias = [item for item in incidencias if item.get("estado") == estado]
    if prioridad:
        incidencias = [item for item in incidencias if item.get("prioridad") == prioridad]

    total = len(incidencias)
    resultados = incidencias[offset : offset + limit]
    return jsonify({"total": total, "resultados": resultados})


@app.post("/incidencias")
@require_auth
def create_incidencia() -> Any:
    payload = request.get_json(silent=True) or {}

    titulo = (payload.get("titulo") or "").strip()
    descripcion = (payload.get("descripcion") or "").strip()
    reportado_por = (payload.get("reportado_por") or "").strip()
    prioridad_manual = payload.get("prioridad")
    categoria = (payload.get("categoria") or "soporte").strip()

    if not titulo or len(titulo) > 200:
        return jsonify({"error": "El título es obligatorio (1-200 caracteres)"}), 400
    if len(descripcion) < 10 or len(descripcion) > 2000:
        return jsonify({"error": "La descripción debe tener entre 10 y 2000 caracteres"}), 400
    if not EMAIL_PATTERN.match(reportado_por):
        return jsonify({"error": "reportado_por debe ser un email válido"}), 400
    if prioridad_manual and prioridad_manual not in VALID_PRIORIDADES:
        return jsonify({"error": "Prioridad inválida"}), 400

    incidencias = storage.load()
    classification = classify_incidencia(titulo, descripcion, prioridad_manual)

    nueva = {
        "id": _next_id(incidencias),
        "titulo": titulo,
        "descripcion": descripcion,
        "estado": "abierta",
        "prioridad": classification.prioridad,
        "clasificacion": classification.clasificacion,
        "clasificacion_automatica": classification.clasificacion,
        "confianza_clasificacion": classification.confianza,
        "categoria": categoria,
        "reportado_por": reportado_por,
        "fecha_creacion": _utc_now(),
        "asignado_a": "soporte_equipo",
    }

    incidencias.append(nueva)
    storage.save(incidencias)
    return jsonify(nueva), 201


@app.get("/metricas")
@require_auth
def metricas() -> Any:
    incidencias = storage.load()
    por_prioridad = {"baja": 0, "media": 0, "alta": 0}
    por_estado = {"abierta": 0, "en_proceso": 0, "cerrada": 0}

    for item in incidencias:
        prioridad = item.get("prioridad", "media")
        estado = item.get("estado", "abierta")
        if prioridad in por_prioridad:
            por_prioridad[prioridad] += 1
        if estado in por_estado:
            por_estado[estado] += 1

    return jsonify(
        {
            "total_incidencias": len(incidencias),
            "por_prioridad": por_prioridad,
            "por_estado": por_estado,
            "timestamp": _utc_now(),
        }
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG") == "1")
