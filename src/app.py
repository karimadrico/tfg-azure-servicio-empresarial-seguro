from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from pathlib import Path
from typing import Any, Callable

from flask import Flask, Response, jsonify, request, send_from_directory

from catalog import catalog_as_list, default_selection, resolve_service_context
from classifier import VALID_TIPOS, classify_solicitud
from config import Config
from operations import build_csv_report, build_operational_summary
from request_workflow import (
    apply_approval_decision,
    apply_escalation,
    initial_workflow_fields,
    mark_approval_notification,
)
from storage import IncidenciaStorage

# API REST sin sesiones por cookie; los endpoints protegidos usan Bearer token.
app = Flask(__name__, static_folder="static")  # NOSONAR
config = Config()
storage = IncidenciaStorage(config)

VALID_ESTADOS = {"pendiente_aprobacion", "abierta", "en_proceso", "cerrada", "rechazada"}
VALID_PRIORIDADES = {"baja", "media", "alta"}
TRANSICIONES_ESTADO = {
    "pendiente_aprobacion": set(),
    "abierta": {"en_proceso", "cerrada"},
    "en_proceso": {"abierta", "cerrada"},
    "cerrada": {"en_proceso"},
    "rechazada": set(),
}
SLA_HORAS = {"alta": 4, "media": 24, "baja": 72}
UTC_OFFSET = "+00:00"
PRIORIDAD_INVALIDA = "Prioridad inválida"
SOLICITUD_NO_ENCONTRADA = "Solicitud no encontrada"


@app.after_request
def add_security_headers(response: Any) -> Any:
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    return response


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(UTC_OFFSET, "Z")


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
    created = datetime.fromisoformat(created_at.replace("Z", UTC_OFFSET))
    deadline = created + timedelta(hours=SLA_HORAS[prioridad])
    return deadline.replace(microsecond=0).isoformat().replace(UTC_OFFSET, "Z")


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


def _validate_required_fields(titulo: str, descripcion: str, reportado_por: str) -> str | None:
    if not titulo or len(titulo) > 200:
        return "El título es obligatorio (1-200 caracteres)"
    if len(descripcion) < 10 or len(descripcion) > 2000:
        return "La descripción debe tener entre 10 y 2000 caracteres"
    if not _is_valid_email(reportado_por):
        return "reportado_por debe ser un email válido"
    return None


def _validate_solicitud_payload(payload: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    titulo = (payload.get("titulo") or "").strip()
    descripcion = (payload.get("descripcion") or "").strip()
    reportado_por = (payload.get("reportado_por") or "").strip()
    prioridad_manual = payload.get("prioridad")
    tipo_solicitud = (payload.get("tipo_solicitud") or "incidencia").strip()
    categoria = (payload.get("categoria") or "soporte").strip()
    default_service, default_asset, default_environment = default_selection()
    service_id = (payload.get("servicio_id") or default_service).strip()
    asset_id = (payload.get("activo_id") or default_asset).strip()
    environment = (payload.get("entorno") or default_environment).strip()

    required_error = _validate_required_fields(titulo, descripcion, reportado_por)
    if required_error:
        return None, required_error
    if prioridad_manual and prioridad_manual not in VALID_PRIORIDADES:
        return None, PRIORIDAD_INVALIDA
    if tipo_solicitud not in VALID_TIPOS:
        return None, "tipo_solicitud inválido"

    return {
        "titulo": titulo,
        "descripcion": descripcion,
        "reportado_por": reportado_por,
        "prioridad_manual": prioridad_manual,
        "tipo_solicitud": tipo_solicitud,
        "categoria": categoria,
        "servicio_id": service_id,
        "activo_id": asset_id,
        "entorno": environment,
    }, None


def _create_solicitud_record(validated: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    incidencias = storage.load()
    classification = classify_solicitud(
        validated["titulo"],
        validated["descripcion"],
        validated.get("prioridad_manual"),
        validated["tipo_solicitud"],
    )
    service_context, service_error = resolve_service_context(
        validated["servicio_id"],
        validated["activo_id"],
        validated["entorno"],
        classification.prioridad,
    )
    if service_error:
        return None, service_error
    if service_context is None:
        return None, "No se pudo resolver el servicio"

    created_at = _utc_now()
    workflow_fields = initial_workflow_fields(
        classification.tipo_solicitud, service_context, created_at
    )
    nueva = {
        "id": _next_id(incidencias),
        "titulo": validated["titulo"],
        "descripcion": validated["descripcion"],
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
        "asignado_a": service_context["propietario_servicio"],
        "historial": [
            {
                "fecha": created_at,
                "accion": "creacion",
                "actor": validated["reportado_por"],
                "detalle": "Solicitud registrada y clasificada automáticamente.",
            }
        ],
    }

    nueva.update(service_context)
    nueva.update(workflow_fields)
    incidencias.append(nueva)
    storage.save(incidencias)
    return nueva, None


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
        return jsonify({"error": SOLICITUD_NO_ENCONTRADA}), 404
    return jsonify(solicitud)


def _validate_state_transition(new_state: str, current_state: str) -> tuple[str, int] | None:
    if new_state and new_state not in VALID_ESTADOS:
        return "Estado inválido", 400
    if new_state and new_state != current_state and new_state not in TRANSICIONES_ESTADO[current_state]:
        return f"No se puede pasar de {current_state} a {new_state}", 409
    return None


def _validate_update_values(payload: dict[str, Any], values: dict[str, str]) -> tuple[str, int] | None:
    if values["prioridad"] and values["prioridad"] not in VALID_PRIORIDADES:
        return PRIORIDAD_INVALIDA, 400
    if "asignado_a" in payload and (not values["asignado_a"] or len(values["asignado_a"]) > 100):
        return "asignado_a debe tener entre 1 y 100 caracteres", 400
    if len(values["comentario"]) > 500 or not values["actor"] or len(values["actor"]) > 100:
        return "Comentario o actor inválido", 400
    return None


def _validate_update_payload(
    payload: dict[str, Any], solicitud: dict[str, Any]
) -> tuple[dict[str, str] | None, tuple[str, int] | None]:
    allowed_fields = {"estado", "prioridad", "asignado_a", "comentario", "actor"}
    if not payload or any(field not in allowed_fields for field in payload):
        return None, ("La actualización contiene campos no permitidos", 400)

    values = {
        "estado": payload.get("estado") or "",
        "prioridad": payload.get("prioridad") or "",
        "asignado_a": (payload.get("asignado_a") or "").strip(),
        "comentario": (payload.get("comentario") or "").strip(),
        "actor": (payload.get("actor") or "equipo_ti").strip(),
    }
    validation_error = _validate_state_transition(values["estado"], solicitud["estado"])
    if validation_error is None:
        validation_error = _validate_update_values(payload, values)
    if validation_error:
        return None, validation_error
    return values, None


def _apply_update_values(solicitud: dict[str, Any], values: dict[str, str]) -> list[str]:
    changes: list[str] = []
    if values["estado"] and values["estado"] != solicitud["estado"]:
        changes.append(f"Estado: {solicitud['estado']} -> {values['estado']}")
        solicitud["estado"] = values["estado"]
    if values["prioridad"] and values["prioridad"] != solicitud["prioridad"]:
        changes.append(f"Prioridad: {solicitud['prioridad']} -> {values['prioridad']}")
        solicitud["prioridad"] = values["prioridad"]
        solicitud["fecha_objetivo_sla"] = _sla_deadline(
            solicitud["fecha_creacion"], values["prioridad"]
        )
    if values["asignado_a"] and values["asignado_a"] != solicitud.get("asignado_a"):
        previous = solicitud.get("asignado_a", "sin asignar")
        changes.append(f"Asignación: {previous} -> {values['asignado_a']}")
        solicitud["asignado_a"] = values["asignado_a"]
    if values["comentario"]:
        changes.append(f"Nota: {values['comentario']}")
    return changes


@app.patch("/solicitudes/<solicitud_id>")
@require_auth
def update_solicitud(solicitud_id: str) -> Any:
    payload = request.get_json(silent=True) or {}
    incidencias = storage.load()
    solicitud = _find_solicitud(incidencias, solicitud_id)
    if solicitud is None:
        return jsonify({"error": SOLICITUD_NO_ENCONTRADA}), 404

    values, validation_error = _validate_update_payload(payload, solicitud)
    if validation_error:
        message, status = validation_error
        return jsonify({"error": message}), status

    previous_state = solicitud["estado"]
    changes = _apply_update_values(solicitud, values or {})
    if not changes:
        return jsonify({"error": "No se han indicado cambios"}), 400

    updated_at = _utc_now()
    solicitud["fecha_actualizacion"] = updated_at
    if solicitud["estado"] == "cerrada" and previous_state != "cerrada":
        solicitud["fecha_cierre"] = updated_at
    elif previous_state == "cerrada" and solicitud["estado"] != "cerrada":
        solicitud["fecha_cierre"] = None
    solicitud.setdefault("historial", []).append(
        {
            "fecha": updated_at,
            "accion": "actualizacion",
            "actor": values["actor"],
            "detalle": "; ".join(changes),
        }
    )
    storage.save(incidencias)
    return jsonify(solicitud)


def _workflow_record(solicitud_id: str) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    records = storage.load()
    return records, _find_solicitud(records, solicitud_id)


def _demo_payloads() -> tuple[dict[str, str], ...]:
    return (
        {
            "tipo_solicitud": "acceso",
            "titulo": "[DEMO] Acceso VPN para consultora externa",
            "descripcion": "Acceso temporal a la VPN corporativa para una consultora durante la auditoria.",
            "reportado_por": "auditoria@empresa.com",
            "servicio_id": "vpn",
            "activo_id": "grupo-acceso-vpn",
            "entorno": "produccion",
        },
        {
            "tipo_solicitud": "incidencia",
            "titulo": "[DEMO] Servicio financiero no disponible",
            "descripcion": "El portal financiero de produccion no responde y bloquea el cierre contable.",
            "reportado_por": "finanzas@empresa.com",
            "servicio_id": "aplicacion-finanzas",
            "activo_id": "portal-finanzas",
            "entorno": "produccion",
            "prioridad": "alta",
        },
        {
            "tipo_solicitud": "configuracion",
            "titulo": "[DEMO] Ajuste de configuracion en preproduccion",
            "descripcion": "Actualizar la configuracion de App Service antes de la validacion funcional.",
            "reportado_por": "cloud@empresa.com",
            "servicio_id": "plataforma-cloud",
            "activo_id": "app-service",
            "entorno": "preproduccion",
        },
        {
            "tipo_solicitud": "incidencia",
            "titulo": "[DEMO] Incidencia de correo resuelta",
            "descripcion": "Un buzon compartido no sincronizaba los mensajes del equipo comercial.",
            "reportado_por": "comercial@empresa.com",
            "servicio_id": "correo",
            "activo_id": "buzon-usuario",
            "entorno": "corporativo",
        },
        {
            "tipo_solicitud": "incidencia",
            "titulo": "[DEMO] Degradacion del gateway VPN",
            "descripcion": "La latencia del gateway VPN afecta a varios usuarios que trabajan en remoto.",
            "reportado_por": "operaciones@empresa.com",
            "servicio_id": "vpn",
            "activo_id": "gateway-vpn",
            "entorno": "corporativo",
        },
    )


def _prepare_demo_records(records: list[dict[str, Any]]) -> None:
    now = datetime.now(timezone.utc).replace(microsecond=0)
    by_title = {item["titulo"]: item for item in records}

    overdue = by_title["[DEMO] Servicio financiero no disponible"]
    overdue["fecha_creacion"] = (now - timedelta(hours=10)).isoformat().replace(
        UTC_OFFSET, "Z"
    )
    overdue["fecha_inicio_sla"] = overdue["fecha_creacion"]
    overdue["fecha_objetivo_sla"] = (now - timedelta(hours=6)).isoformat().replace(
        UTC_OFFSET, "Z"
    )

    in_progress = by_title["[DEMO] Ajuste de configuracion en preproduccion"]
    in_progress["estado"] = "en_proceso"
    in_progress["estado_aprobacion"] = "aprobada"
    in_progress["fecha_decision"] = _utc_now()
    in_progress.setdefault("historial", []).append(
        {
            "fecha": _utc_now(),
            "accion": "asignacion",
            "actor": "equipo_cloud",
            "detalle": "Cambio aprobado y asignado al equipo cloud.",
        }
    )

    closed = by_title["[DEMO] Incidencia de correo resuelta"]
    closed["estado"] = "cerrada"
    closed["fecha_cierre"] = _utc_now()
    closed.setdefault("historial", []).append(
        {
            "fecha": _utc_now(),
            "accion": "cierre",
            "actor": "equipo_colaboracion",
            "detalle": "Sincronizacion restablecida y validada con el usuario.",
        }
    )

    escalated = by_title["[DEMO] Degradacion del gateway VPN"]
    apply_escalation(
        escalated,
        "centro_operaciones",
        "Afectacion simultanea a varios usuarios",
        _utc_now(),
    )

    for record in records:
        record["es_demo"] = True


@app.post("/demo/cargar")
@require_auth
def load_demo_data() -> Any:
    records = storage.load()
    existing = [item for item in records if item.get("es_demo")]
    if existing:
        return jsonify({"creadas": 0, "existentes": len(existing), "solicitudes": existing})

    for payload in _demo_payloads():
        validated, error = _validate_solicitud_payload(payload)
        if error or validated is None:
            return jsonify({"error": error or "Datos de demostracion invalidos"}), 500
        record, service_error = _create_solicitud_record(validated)
        if service_error or record is None:
            return jsonify({"error": service_error or "No se pudo crear la demostracion"}), 500

    records = storage.load()
    demo_records = [item for item in records if item.get("titulo", "").startswith("[DEMO]")]
    _prepare_demo_records(demo_records)
    storage.save(records)
    return jsonify({"creadas": len(demo_records), "existentes": 0, "solicitudes": demo_records}), 201


@app.post("/solicitudes/<solicitud_id>/aprobacion")
@require_auth
def decide_approval(solicitud_id: str) -> Any:
    payload = request.get_json(silent=True) or {}
    records, solicitud = _workflow_record(solicitud_id)
    if solicitud is None:
        return jsonify({"error": SOLICITUD_NO_ENCONTRADA}), 404

    decided_at = _utc_now()
    _, error = apply_approval_decision(
        solicitud,
        (payload.get("decision") or "").strip(),
        (payload.get("actor") or "").strip(),
        (payload.get("comentario") or "").strip(),
        decided_at,
    )
    if error:
        return jsonify({"error": error}), 409
    if solicitud["estado_aprobacion"] == "aprobada":
        solicitud["fecha_inicio_sla"] = decided_at
        solicitud["fecha_objetivo_sla"] = _sla_deadline(decided_at, solicitud["prioridad"])
    storage.save(records)
    return jsonify(solicitud)


@app.post("/solicitudes/<solicitud_id>/escalar")
@require_auth
def escalate_solicitud(solicitud_id: str) -> Any:
    payload = request.get_json(silent=True) or {}
    records, solicitud = _workflow_record(solicitud_id)
    if solicitud is None:
        return jsonify({"error": SOLICITUD_NO_ENCONTRADA}), 404

    escalated_at = _utc_now()
    _, error = apply_escalation(
        solicitud,
        (payload.get("actor") or "").strip(),
        (payload.get("motivo") or "").strip(),
        escalated_at,
    )
    if error:
        return jsonify({"error": error}), 409
    solicitud["fecha_objetivo_sla"] = _sla_deadline(escalated_at, "alta")
    storage.save(records)
    return jsonify(solicitud)


@app.post("/solicitudes/<solicitud_id>/notificar-aprobacion")
@require_auth
def notify_approval(solicitud_id: str) -> Any:
    records, solicitud = _workflow_record(solicitud_id)
    if solicitud is None:
        return jsonify({"error": SOLICITUD_NO_ENCONTRADA}), 404

    error = mark_approval_notification(solicitud, "logic_app", _utc_now())
    if error:
        return jsonify({"error": error}), 409
    storage.save(records)
    return jsonify(solicitud)


@app.get("/catalogo")
def catalogo() -> Any:
    return jsonify({"servicios": catalog_as_list()})


@app.get("/incidencias")
@require_auth
def list_incidencias() -> Any:
    estado = request.args.get("estado")
    prioridad = request.args.get("prioridad")
    tipo = request.args.get("tipo_solicitud")
    servicio = request.args.get("servicio_id")
    impacto = request.args.get("impacto")
    limit = request.args.get("limit", default=50, type=int)
    offset = request.args.get("offset", default=0, type=int)

    if estado and estado not in VALID_ESTADOS:
        return jsonify({"error": "Estado inválido"}), 400
    if prioridad and prioridad not in VALID_PRIORIDADES:
            return jsonify({"error": PRIORIDAD_INVALIDA}), 400
    if tipo and tipo not in VALID_TIPOS:
        return jsonify({"error": "tipo_solicitud inválido"}), 400
    if impacto and impacto not in {"bajo", "medio", "alto", "critico"}:
        return jsonify({"error": "impacto inválido"}), 400
    if limit < 1 or limit > 100 or offset < 0:
        return jsonify({"error": "Parámetros de paginación inválidos"}), 400

    incidencias = storage.load()
    if estado:
        incidencias = [item for item in incidencias if item.get("estado") == estado]
    if prioridad:
        incidencias = [item for item in incidencias if item.get("prioridad") == prioridad]
    if tipo:
        incidencias = [item for item in incidencias if item.get("tipo_solicitud") == tipo]
    if servicio:
        incidencias = [item for item in incidencias if item.get("servicio_id") == servicio]
    if impacto:
        incidencias = [item for item in incidencias if item.get("impacto") == impacto]

    total = len(incidencias)
    resultados = incidencias[offset : offset + limit]
    return jsonify({"total": total, "resultados": resultados})


@app.post("/incidencias")
def create_incidencia() -> Any:
    payload = request.get_json(silent=True) or {}
    validated, error = _validate_solicitud_payload(payload)
    if error:
        return jsonify({"error": error}), 400

    nueva, service_error = _create_solicitud_record(validated)
    if service_error:
        return jsonify({"error": service_error}), 400
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
            if deadline_value and datetime.fromisoformat(deadline_value.replace("Z", UTC_OFFSET)) < now:
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


@app.get("/operaciones")
@require_auth
def operations_center() -> Any:
    summary = build_operational_summary(storage.load())
    summary["timestamp"] = _utc_now()
    return jsonify(summary)


@app.get("/informes/solicitudes.csv")
@require_auth
def export_requests_csv() -> Response:
    return Response(
        build_csv_report(storage.load()),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=solicitudes-ti.csv"},
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    app.run(host=host, port=port, debug=os.getenv("FLASK_DEBUG") == "1")
