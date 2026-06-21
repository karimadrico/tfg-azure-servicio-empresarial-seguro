from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from pathlib import Path
from typing import Any, Callable

from flask import Flask, jsonify, request, send_from_directory

from classifier import VALID_TIPOS, classify_solicitud
from config import Config
from storage import IncidenciaStorage

# API REST sin sesiones por cookie; los endpoints protegidos usan Bearer token.
app = Flask(__name__, static_folder="static")  # NOSONAR
config = Config()
storage = IncidenciaStorage(config)

VALID_ESTADOS = {"abierta", "en_proceso", "cerrada"}
VALID_PRIORIDADES = {"baja", "media", "alta"}
TRANSICIONES_ESTADO = {
    "abierta": {"en_proceso", "cerrada"},
    "en_proceso": {"abierta", "cerrada"},
    "cerrada": {"en_proceso"},
}
SLA_HORAS = {"alta": 4, "media": 24, "baja": 72}


@app.after_request
def add_security_headers(response: Any) -> Any:
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    return response


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _next_id(incidencias: list[dict[str, Any]]) -> str:
    if not incidencias:
        return "SOL-001"
    numbers = []
    for item in incidencias:
        identifier = str(item.get("id", ""))
        prefix, separator, number = identifier.partition("-")
        if separator and prefix in {"SOL", "INC"} and number.isdecimal():
            numbers.append(int(number))
    return f"SOL-{max(numbers, default=0) + 1:03d}"


def _find_solicitud(incidencias: list[dict[str, Any]], solicitud_id: str) -> dict[str, Any] | None:
    return next((item for item in incidencias if item.get("id") == solicitud_id), None)


def _sla_deadline(created_at: str, prioridad: str) -> str:
    created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    deadline = created + timedelta(hours=SLA_HORAS[prioridad])
    return deadline.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _is_valid_email(value: str) -> bool:
    if not value or len(value) > 254 or value.count("@") != 1:
        return False

    local_part, domain = value.split("@", 1)
    if not local_part or not domain or len(local_part) > 64:
        return False
    if any(char.isspace() for char in value):
        return False
    if "." not in domain or domain.startswith(".") or domain.endswith("."):
        return False

    return all(label and not label.startswith("-") and not label.endswith("-") for label in domain.split("."))


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


def _validate_solicitud_payload(payload: dict[str, Any]) -> tuple[dict[str, str] | None, str | None]:
    titulo = (payload.get("titulo") or "").strip()
    descripcion = (payload.get("descripcion") or "").strip()
    reportado_por = (payload.get("reportado_por") or "").strip()
    prioridad_manual = payload.get("prioridad")
    tipo_solicitud = (payload.get("tipo_solicitud") or "incidencia").strip()
    categoria = (payload.get("categoria") or "soporte").strip()

    if not titulo or len(titulo) > 200:
        return None, "El título es obligatorio (1-200 caracteres)"
    if len(descripcion) < 10 or len(descripcion) > 2000:
        return None, "La descripción debe tener entre 10 y 2000 caracteres"
    if not _is_valid_email(reportado_por):
        return None, "reportado_por debe ser un email válido"
    if prioridad_manual and prioridad_manual not in VALID_PRIORIDADES:
        return None, "Prioridad inválida"
    if tipo_solicitud not in VALID_TIPOS:
        return None, "tipo_solicitud inválido"

    return {
        "titulo": titulo,
        "descripcion": descripcion,
        "reportado_por": reportado_por,
        "prioridad_manual": prioridad_manual,
        "tipo_solicitud": tipo_solicitud,
        "categoria": categoria,
    }, None


def _create_solicitud_record(validated: dict[str, str]) -> dict[str, Any]:
    incidencias = storage.load()
    classification = classify_solicitud(
        validated["titulo"],
        validated["descripcion"],
        validated.get("prioridad_manual"),
        validated["tipo_solicitud"],
    )

    created_at = _utc_now()
    nueva = {
        "id": _next_id(incidencias),
        "titulo": validated["titulo"],
        "descripcion": validated["descripcion"],
        "estado": "abierta",
        "prioridad": classification.prioridad,
        "tipo_solicitud": classification.tipo_solicitud,
        "clasificacion": classification.clasificacion,
        "clasificacion_automatica": classification.clasificacion,
        "confianza_clasificacion": classification.confianza,
        "recomendacion": classification.recomendacion,
        "categoria": validated["categoria"],
        "reportado_por": validated["reportado_por"],
        "fecha_creacion": created_at,
        "fecha_actualizacion": created_at,
        "fecha_objetivo_sla": _sla_deadline(created_at, classification.prioridad),
        "asignado_a": "equipo_cloud",
        "historial": [
            {
                "fecha": created_at,
                "accion": "creacion",
                "actor": validated["reportado_por"],
                "detalle": "Solicitud registrada y clasificada automáticamente.",
            }
        ],
    }

    incidencias.append(nueva)
    storage.save(incidencias)
    return nueva


@app.get("/")
def root() -> Any:
    return jsonify(
        {
            "mensaje": "Plataforma TFG — Automatización de Solicitudes TI en Azure",
            "version": "2.0",
            "estado": "operacional",
            "portal": "/portal",
            "timestamp": _utc_now(),
        }
    )


@app.get("/portal")
def portal() -> Any:
    return send_from_directory(Path(app.static_folder), "index.html")


@app.get("/health")
def health() -> Any:
    return jsonify(
        {
            "estado": "ok",
            "storage_mode": config.STORAGE_MODE,
            "timestamp": _utc_now(),
        }
    )


@app.get("/solicitudes")
@require_auth
def list_solicitudes() -> Any:
    return list_incidencias()


@app.post("/solicitudes")
def create_solicitud() -> Any:
    return create_incidencia()


@app.get("/solicitudes/<solicitud_id>")
@require_auth
def get_solicitud(solicitud_id: str) -> Any:
    solicitud = _find_solicitud(storage.load(), solicitud_id)
    if solicitud is None:
        return jsonify({"error": "Solicitud no encontrada"}), 404
    return jsonify(solicitud)


@app.patch("/solicitudes/<solicitud_id>")
@require_auth
def update_solicitud(solicitud_id: str) -> Any:
    payload = request.get_json(silent=True) or {}
    allowed_fields = {"estado", "prioridad", "asignado_a", "comentario", "actor"}
    if not payload or any(field not in allowed_fields for field in payload):
        return jsonify({"error": "La actualización contiene campos no permitidos"}), 400

    incidencias = storage.load()
    solicitud = _find_solicitud(incidencias, solicitud_id)
    if solicitud is None:
        return jsonify({"error": "Solicitud no encontrada"}), 404

    estado = payload.get("estado")
    prioridad = payload.get("prioridad")
    asignado_a = (payload.get("asignado_a") or "").strip()
    comentario = (payload.get("comentario") or "").strip()
    actor = (payload.get("actor") or "equipo_ti").strip()

    if estado and estado not in VALID_ESTADOS:
        return jsonify({"error": "Estado inválido"}), 400
    if estado and estado != solicitud["estado"] and estado not in TRANSICIONES_ESTADO[solicitud["estado"]]:
        return jsonify({"error": f"No se puede pasar de {solicitud['estado']} a {estado}"}), 409
    if prioridad and prioridad not in VALID_PRIORIDADES:
        return jsonify({"error": "Prioridad inválida"}), 400
    if "asignado_a" in payload and (not asignado_a or len(asignado_a) > 100):
        return jsonify({"error": "asignado_a debe tener entre 1 y 100 caracteres"}), 400
    if len(comentario) > 500 or not actor or len(actor) > 100:
        return jsonify({"error": "Comentario o actor inválido"}), 400

    changes: list[str] = []
    if estado and estado != solicitud["estado"]:
        changes.append(f"Estado: {solicitud['estado']} -> {estado}")
        solicitud["estado"] = estado
    if prioridad and prioridad != solicitud["prioridad"]:
        changes.append(f"Prioridad: {solicitud['prioridad']} -> {prioridad}")
        solicitud["prioridad"] = prioridad
        solicitud["fecha_objetivo_sla"] = _sla_deadline(solicitud["fecha_creacion"], prioridad)
    if asignado_a and asignado_a != solicitud.get("asignado_a"):
        changes.append(f"Asignación: {solicitud.get('asignado_a', 'sin asignar')} -> {asignado_a}")
        solicitud["asignado_a"] = asignado_a
    if comentario:
        changes.append(f"Nota: {comentario}")
    if not changes:
        return jsonify({"error": "No se han indicado cambios"}), 400

    updated_at = _utc_now()
    solicitud["fecha_actualizacion"] = updated_at
    solicitud.setdefault("historial", []).append(
        {
            "fecha": updated_at,
            "accion": "actualizacion",
            "actor": actor,
            "detalle": "; ".join(changes),
        }
    )
    storage.save(incidencias)
    return jsonify(solicitud)


@app.get("/incidencias")
@require_auth
def list_incidencias() -> Any:
    estado = request.args.get("estado")
    prioridad = request.args.get("prioridad")
    tipo = request.args.get("tipo_solicitud")
    limit = request.args.get("limit", default=50, type=int)
    offset = request.args.get("offset", default=0, type=int)

    if estado and estado not in VALID_ESTADOS:
        return jsonify({"error": "Estado inválido"}), 400
    if prioridad and prioridad not in VALID_PRIORIDADES:
        return jsonify({"error": "Prioridad inválida"}), 400
    if tipo and tipo not in VALID_TIPOS:
        return jsonify({"error": "tipo_solicitud inválido"}), 400
    if limit < 1 or limit > 100 or offset < 0:
        return jsonify({"error": "Parámetros de paginación inválidos"}), 400

    incidencias = storage.load()
    if estado:
        incidencias = [item for item in incidencias if item.get("estado") == estado]
    if prioridad:
        incidencias = [item for item in incidencias if item.get("prioridad") == prioridad]
    if tipo:
        incidencias = [item for item in incidencias if item.get("tipo_solicitud") == tipo]

    total = len(incidencias)
    resultados = incidencias[offset : offset + limit]
    return jsonify({"total": total, "resultados": resultados})


@app.post("/incidencias")
def create_incidencia() -> Any:
    payload = request.get_json(silent=True) or {}
    validated, error = _validate_solicitud_payload(payload)
    if error:
        return jsonify({"error": error}), 400

    nueva = _create_solicitud_record(validated)
    return jsonify(nueva), 201


@app.get("/metricas")
@require_auth
def metricas() -> Any:
    incidencias = storage.load()
    por_prioridad = {"baja": 0, "media": 0, "alta": 0}
    por_estado = {"abierta": 0, "en_proceso": 0, "cerrada": 0}
    por_tipo = dict.fromkeys(VALID_TIPOS, 0)
    sla = {"en_plazo": 0, "vencidas": 0, "cerradas": 0}
    now = datetime.now(timezone.utc)

    for item in incidencias:
        prioridad = item.get("prioridad", "media")
        estado = item.get("estado", "abierta")
        tipo = item.get("tipo_solicitud", "incidencia")
        if prioridad in por_prioridad:
            por_prioridad[prioridad] += 1
        if estado in por_estado:
            por_estado[estado] += 1
        if tipo in por_tipo:
            por_tipo[tipo] += 1
        if estado == "cerrada":
            sla["cerradas"] += 1
        else:
            deadline_value = item.get("fecha_objetivo_sla")
            if deadline_value and datetime.fromisoformat(deadline_value.replace("Z", "+00:00")) < now:
                sla["vencidas"] += 1
            else:
                sla["en_plazo"] += 1

    return jsonify(
        {
            "total_solicitudes": len(incidencias),
            "por_prioridad": por_prioridad,
            "por_estado": por_estado,
            "por_tipo_solicitud": por_tipo,
            "sla": sla,
            "timestamp": _utc_now(),
        }
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    app.run(host=host, port=port, debug=os.getenv("FLASK_DEBUG") == "1")
