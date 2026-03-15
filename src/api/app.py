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
    incidencias.append(data)
    return jsonify({"mensaje": "Incidencia creada"}), 201

@app.route("/metricas", methods=["GET"])
def metricas():
    return jsonify({
        "total_incidencias": len(incidencias)
    })

if __name__ == "__main__":
    app.run()