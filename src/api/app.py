from flask import Flask, jsonify, request

app = Flask(__name__)

incidencias = []

@app.route("/")
def home():
    return jsonify({"mensaje": "API TFG Servicio Empresarial Seguro"})

@app.route("/incidencias", methods=["GET"])
def obtener_incidencias():
    return jsonify(incidencias)

@app.route("/incidencias", methods=["POST"])
def crear_incidencia():
    data = request.json

    if not data or "titulo" not in data:
        return jsonify({"error": "El campo titulo es obligatorio"}), 400

    incidencias.append(data)

    return jsonify({
        "mensaje": "Incidencia creada",
        "total": len(incidencias)
    }), 201


@app.route("/metricas", methods=["GET"])
def metricas():
    return jsonify({
        "total_incidencias": len(incidencias)
    })


if __name__ == "__main__":
    app.run()