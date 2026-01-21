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

    # Lógica de precio
    if cantidad >= 60:
        precio = precio_promo
        tipo_precio = "Precio PROMOCIÓN aplicado"
    else:
        precio = precio_normal
        tipo_precio = "Precio normal"

    total = cantidad * precio

    # Lógica de despacho
    if cantidad >= 12:
        despacho = (
            "🚚 Despacho a domicilio GRATIS dentro de Coyhaique.\n"
            "Un ejecutivo coordinará día y horario de entrega."
        )
    else:
        despacho = (
            "📍 Retiro en sucursal Coyhaique.\n"
            "Dirección: Lautaro #257."
        )

    mensaje = f"""
🔥 Cotización de Pellet – Coyhaique

• Producto: Pellet certificado (saco 15 kg)
• Cantidad solicitada: {cantidad} sacos
• Precio por saco: ${precio:,}
• Total estimado: ${total:,}

{tipo_precio}

{despacho}
"""

    return jsonify({
        "cantidad": cantidad,
        "precio_saco": precio,
        "total": total,
        "mensaje": mensaje.strip()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
