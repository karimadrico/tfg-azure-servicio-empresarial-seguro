"""Reglas de aprobacion y escalado de solicitudes empresariales."""

from __future__ import annotations

from typing import Any


VALID_APPROVAL_DECISIONS = {"aprobar", "rechazar"}


def requires_approval(request_type: str, context: dict[str, str]) -> bool:
    sensitive_type = request_type in {"acceso", "configuracion"}
    sensitive_service = context["criticidad_servicio"] in {"alta", "critica"}
    sensitive_environment = context["entorno"] == "produccion"
    return sensitive_type and (sensitive_service or sensitive_environment)


def initial_workflow_fields(
    request_type: str,
    context: dict[str, str],
    created_at: str,
) -> dict[str, Any]:
    approval_required = requires_approval(request_type, context)
    return {
        "estado": "pendiente_aprobacion" if approval_required else "abierta",
        "requiere_aprobacion": approval_required,
        "estado_aprobacion": "pendiente" if approval_required else "no_requerida",
        "aprobador": context["aprobador_servicio"] if approval_required else "",
        "fecha_decision": None,
        "notificacion_aprobacion": None,
        "nivel_escalado": 0,
        "fecha_escalado": None,
        "motivo_escalado": "",
        "fecha_cierre": None,
        "fecha_inicio_sla": created_at,
    }


def apply_approval_decision(
    request_record: dict[str, Any],
    decision: str,
    actor: str,
    comment: str,
    decided_at: str,
) -> tuple[str | None, str | None]:
    if not request_record.get("requiere_aprobacion"):
        return None, "La solicitud no requiere aprobacion"
    if request_record.get("estado_aprobacion") != "pendiente":
        return None, "La solicitud ya tiene una decision"
    if decision not in VALID_APPROVAL_DECISIONS:
        return None, "decision debe ser aprobar o rechazar"
    if not actor or len(actor) > 100 or len(comment) > 500:
        return None, "Actor o comentario de aprobacion invalido"

    approved = decision == "aprobar"
    request_record["estado_aprobacion"] = "aprobada" if approved else "rechazada"
    request_record["estado"] = "abierta" if approved else "rechazada"
    request_record["fecha_decision"] = decided_at
    request_record["fecha_actualizacion"] = decided_at
    if not approved:
        request_record["fecha_cierre"] = decided_at

    detail = f"Decision: {request_record['estado_aprobacion']}"
    if comment:
        detail += f"; Motivo: {comment}"
    append_history(request_record, decided_at, "aprobacion", actor, detail)
    return detail, None


def apply_escalation(
    request_record: dict[str, Any],
    actor: str,
    reason: str,
    escalated_at: str,
) -> tuple[str | None, str | None]:
    if request_record.get("estado") in {"cerrada", "rechazada"}:
        return None, "No se puede escalar una solicitud finalizada"
    if not actor or len(actor) > 100 or not reason or len(reason) > 500:
        return None, "Actor y motivo de escalado son obligatorios"

    level = int(request_record.get("nivel_escalado", 0)) + 1
    request_record["nivel_escalado"] = level
    request_record["fecha_escalado"] = escalated_at
    request_record["motivo_escalado"] = reason
    request_record["prioridad"] = "alta"
    request_record["asignado_a"] = request_record.get("propietario_servicio", "equipo_ti")
    request_record["fecha_actualizacion"] = escalated_at
    detail = f"Escalado nivel {level}: {reason}"
    append_history(request_record, escalated_at, "escalado", actor, detail)
    return detail, None


def mark_approval_notification(
    request_record: dict[str, Any], actor: str, notified_at: str
) -> str | None:
    if request_record.get("estado_aprobacion") != "pendiente":
        return "No existe una aprobacion pendiente"
    request_record["notificacion_aprobacion"] = notified_at
    request_record["fecha_actualizacion"] = notified_at
    append_history(
        request_record,
        notified_at,
        "notificacion_aprobacion",
        actor,
        f"Aprobacion notificada a {request_record.get('aprobador', 'responsable')}",
    )
    return None


def append_history(
    request_record: dict[str, Any],
    timestamp: str,
    action: str,
    actor: str,
    detail: str,
) -> None:
    request_record.setdefault("historial", []).append(
        {"fecha": timestamp, "accion": action, "actor": actor, "detalle": detail}
    )
