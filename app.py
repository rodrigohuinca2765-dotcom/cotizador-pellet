from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Cotizador de Pellet activo 🚀"

@app.route("/cotizar", methods=["POST"])
def cotizar():
    data = request.get_json()
    cantidad = int(data.get("cantidad", 0))

    # Precio por saco
    if cantidad >= 60:
        precio = 4240
        promo = "Precio promoción aplicado para compras desde 60 sacos."
    else:
        precio = 4990
        promo = "Compras desde 60 sacos acceden a precio promoción."

    total = cantidad * precio

    # Condición de despacho
    if cantidad >= 12:
        entrega = "Despacho a domicilio sin costo dentro de la comuna de Coyhaique."
    else:
        entrega = "Retiro en sucursal Coyhaique, Lautaro #257."

    mensaje = f"""
Estimado/a 👋

Detalle de su cotización de pellet:

📦 Cantidad: {cantidad} sacos (15 kg c/u)
💰 Precio por saco: ${precio}
🧾 Total estimado: ${total}

🚚 {entrega}

{promo}
"""

    return jsonify({
        "respuesta": mensaje.strip(),
        "precio_saco": precio,
        "total": total
    })
