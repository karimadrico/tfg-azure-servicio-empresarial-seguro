"""Catalogo empresarial de servicios y activos gestionados."""

from __future__ import annotations

from typing import Any


SERVICE_CATALOG: dict[str, dict[str, Any]] = {
    "general": {
        "nombre": "Servicio TI general",
        "descripcion": "Consultas y solicitudes sin servicio especifico.",
        "criticidad": "baja",
        "propietario": "equipo_soporte",
        "aprobador": "responsable_soporte",
        "entornos": ["corporativo"],
        "activos": [{"id": "puesto-usuario", "nombre": "Puesto de usuario"}],
    },
    "vpn": {
        "nombre": "VPN corporativa",
        "descripcion": "Acceso remoto seguro a recursos internos.",
        "criticidad": "alta",
        "propietario": "equipo_seguridad",
        "aprobador": "responsable_seguridad",
        "entornos": ["corporativo", "produccion"],
        "activos": [
            {"id": "gateway-vpn", "nombre": "Gateway VPN"},
            {"id": "grupo-acceso-vpn", "nombre": "Grupo de acceso VPN"},
        ],
    },
    "plataforma-cloud": {
        "nombre": "Plataforma cloud Azure",
        "descripcion": "Recursos y aplicaciones alojados en Microsoft Azure.",
        "criticidad": "alta",
        "propietario": "equipo_cloud",
        "aprobador": "responsable_cloud",
        "entornos": ["desarrollo", "preproduccion", "produccion"],
        "activos": [
            {"id": "app-service", "nombre": "Azure App Service"},
            {"id": "storage-account", "nombre": "Azure Storage Account"},
            {"id": "key-vault", "nombre": "Azure Key Vault"},
        ],
    },
    "aplicacion-finanzas": {
        "nombre": "Aplicacion de finanzas",
        "descripcion": "Servicio empresarial para procesos financieros.",
        "criticidad": "critica",
        "propietario": "equipo_aplicaciones",
        "aprobador": "responsable_finanzas",
        "entornos": ["preproduccion", "produccion"],
        "activos": [
            {"id": "portal-finanzas", "nombre": "Portal financiero"},
            {"id": "api-finanzas", "nombre": "API financiera"},
        ],
    },
    "correo": {
        "nombre": "Correo corporativo",
        "descripcion": "Correo, buzones compartidos y listas de distribucion.",
        "criticidad": "media",
        "propietario": "equipo_colaboracion",
        "aprobador": "responsable_colaboracion",
        "entornos": ["corporativo"],
        "activos": [
            {"id": "buzon-usuario", "nombre": "Buzon de usuario"},
            {"id": "lista-distribucion", "nombre": "Lista de distribucion"},
        ],
    },
    "identidad": {
        "nombre": "Identidad y accesos",
        "descripcion": "Cuentas, grupos, roles y permisos corporativos.",
        "criticidad": "critica",
        "propietario": "equipo_identidad",
        "aprobador": "responsable_identidad",
        "entornos": ["corporativo", "produccion"],
        "activos": [
            {"id": "cuenta-usuario", "nombre": "Cuenta de usuario"},
            {"id": "grupo-seguridad", "nombre": "Grupo de seguridad"},
            {"id": "rol-aplicacion", "nombre": "Rol de aplicacion"},
        ],
    },
}


def catalog_as_list() -> list[dict[str, Any]]:
    return [{"id": service_id, **service} for service_id, service in SERVICE_CATALOG.items()]


def resolve_service_context(
    service_id: str,
    asset_id: str,
    environment: str,
    priority: str,
) -> tuple[dict[str, str] | None, str | None]:
    service = SERVICE_CATALOG.get(service_id)
    if service is None:
        return None, "servicio_id invalido"

    assets = {asset["id"]: asset["nombre"] for asset in service["activos"]}
    if asset_id not in assets:
        return None, "activo_id no pertenece al servicio seleccionado"
    if environment not in service["entornos"]:
        return None, "entorno no permitido para el servicio seleccionado"

    return {
        "servicio_id": service_id,
        "servicio": service["nombre"],
        "activo_id": asset_id,
        "activo": assets[asset_id],
        "entorno": environment,
        "criticidad_servicio": service["criticidad"],
        "impacto": _calculate_impact(service["criticidad"], priority, environment),
        "propietario_servicio": service["propietario"],
        "aprobador_servicio": service["aprobador"],
    }, None


def default_selection() -> tuple[str, str, str]:
    return "general", "puesto-usuario", "corporativo"


def _calculate_impact(criticality: str, priority: str, environment: str) -> str:
    if criticality == "critica" or (criticality == "alta" and priority == "alta"):
        return "critico"
    if criticality == "alta" or priority == "alta" or environment == "produccion":
        return "alto"
    if criticality == "media" or priority == "media":
        return "medio"
    return "bajo"
