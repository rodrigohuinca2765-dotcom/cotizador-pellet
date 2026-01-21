from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Cotizador de Pellet activo 🔥"

@app.route("/cotizar", methods=["POST"])
def cotizar():
    data = request.get_json()
    cantidad = int(data.get("cantidad", 0))

    # Precios
    precio_normal = 4990
    precio_promo = 4240

    # Regla de precio
    if cantidad >= 60:
        precio = precio_promo
        tipo_precio = "Precio PROMOCIÓN aplicado"
    else:
        precio = precio_normal
        tipo_precio = "Precio normal"

    total = cantidad * precio

    # 🚚 Regla de despacho
    if cantidad >= 12:
        despacho = "Despacho a domicilio GRATIS dentro de Coyhaique"
    else:
        despacho = "Retiro en sucursal Coyhaique – Lautaro #257"

    mensaje = (
        "🔥 Cotización de Pellet – Coyhaique\n\n"
        f"📦 Cantidad: {cantidad} sacos (15 kg c/u)\n"
        f"💰 Precio por saco: ${precio}\n"
        f"🧾 Total estimado: ${total}\n\n"
        f"🚚 {despacho}\n"
        f"🏷️ {tipo_precio}"
    )

    return jsonify({
        "cantidad": cantidad,
        "precio_saco": precio,
        "total": total,
        "tipo_precio": tipo_precio,
        "despacho": despacho,
        "mensaje": mensaje
    })
