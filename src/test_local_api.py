import json
import urllib.request

base = "http://127.0.0.1:5000"

for path in ("/health", "/portal", "/"):
    with urllib.request.urlopen(base + path) as response:
        print(path, response.status)
        body = response.read().decode("utf-8", errors="replace")
        print(body[:300])
        print("---")

payload = json.dumps(
    {
        "tipo_solicitud": "acceso",
        "titulo": "Solicitud acceso VPN",
        "descripcion": "Necesito acceso VPN al entorno cloud de desarrollo",
        "reportado_por": "karima@ubu.es",
    }
).encode("utf-8")

req = urllib.request.Request(
    base + "/solicitudes",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(req) as response:
    print("POST /solicitudes", response.status)
    print(response.read().decode("utf-8"))
