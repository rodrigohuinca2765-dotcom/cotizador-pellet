from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 🔓 Permite llamadas desde navegador (Hoppscotch, HTML, etc)

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

    # Lógica de precio
    if cantidad >= 60:
        precio = precio_promo
        tipo_precio = "Precio PROMOCIÓN aplicado (desde 60 sacos)"
    else:
        precio = precio_normal
        tipo_precio = "Precio normal"

    # Lógica de despacho
    if cantidad >= 12:
        despacho = "Despacho a domicilio GRATIS dentro de Coyhaique"
    else:
        despacho = "Retiro en sucursal Coyhaique – Dirección: Lautaro #257"

    total = cantidad * precio

    mensaje = f"""
🔥 Cotización de Pellet – Coyhaique

📦 Cantidad: {cantidad} sacos (15 kg c/u)
💰 Precio por saco: ${precio}
🧾 Total estimado: ${total}

🚚 {despacho}

ℹ️ {tipo_precio}
"""

    return jsonify({
        "cantidad": cantidad,
        "precio_saco": precio,
        "total": total,
        "despacho": despacho,
        "tipo_precio": tipo_precio,
        "mensaje": mensaje.strip()
    })
