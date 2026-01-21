from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Cotizador de Pellet activo 🔥"

@app.route("/cotizar", methods=["POST"])
def cotizar():
    data = request.get_json()
    cantidad = int(data.get("cantidad", 0))

    if cantidad >= 60:
        precio = 4240
        promo = "Precio PROMOCIÓN aplicado."
    else:
        precio = 4990
        promo = "Desde 60 sacos accedes a promoción."

    total = cantidad * precio

    mensaje = f"""
Perfecto 🔥
Tu cotización de {cantidad} sacos:

💰 Precio por saco: ${precio}
🧾 Total: ${total}

📍 Retiro en sucursal Coyhaique
📍 Dirección: Lautaro #257

{promo}
"""

    return jsonify({
        "mensaje": mensaje.strip(),
        "precio_saco": precio,
        "total": total
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
