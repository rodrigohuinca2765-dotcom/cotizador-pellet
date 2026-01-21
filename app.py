from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite llamadas desde Hoppscotch, navegador, etc.


@app.route("/", methods=["GET"])
def home():
    return "Cotizador de Pellet activo 🔥"


@app.route("/cotizar", methods=["POST"])
def cotizar():
    data = request.get_json() or {}
    cantidad = int(data.get("cantidad", 0))

    # Validación básica
    if cantidad <= 0:
        return jsonify({
            "error": "La cantidad debe ser mayor a 0"
        }), 400

    # Precios
    precio_normal = 4990
    precio_promo = 4240

    # Lógica de precio
    if cantidad >= 60:
        precio_saco = precio_promo
        tipo_precio = "Precio PROMOCIÓN aplicado"
    else:
        precio_saco = precio_normal
        tipo_precio = "Precio normal"

    total = cantidad * precio_saco

    # Lógica de despacho
    if cantidad >= 12:
        despacho = "Despacho a domicilio GRATIS dentro de Coyhaique"
    else:
        despacho = "Retiro en sucursal Coyhaique (Lautaro #257)"

    # Mensaje final (para WhatsApp / QR)
    mensaje = (
        "Hola 👋, quiero cotizar pellet en Coyhaique.\n\n"
        "🔥 Pellet certificado – saco 15 kg\n"
        f"📦 Cantidad solicitada: {cantidad} sacos\n"
        f"💰 Precio por saco: ${precio_saco:,}\n"
        f"🧾 Total estimado: ${total:,}\n\n"
        f"🚚 {despacho}\n"
        f"ℹ️ {tipo_precio}"
    )

    return jsonify({
        "cantidad": cantidad,
        "precio_saco": precio_saco,
        "total": total,
        "tipo_precio": tipo_precio,
        "despacho": despacho,
        "mensaje": mensaje
    })
