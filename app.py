from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 🔑 permite llamadas desde GitHub Pages

@app.route("/", methods=["GET"])
def home():
    return "Cotizador de Pellet activo 🔥"

@app.route("/cotizar", methods=["POST"])
def cotizar():
    try:
        data = request.get_json(force=True)
        cantidad = int(data.get("cantidad", 0))

        # Precios
        PRECIO_NORMAL = 4990
        PRECIO_PROMO = 4240

        # Lógica de precio
        if cantidad >= 60:
            precio_saco = PRECIO_PROMO
            tipo_precio = "Precio PROMOCIÓN aplicado"
        else:
            precio_saco = PRECIO_NORMAL
            tipo_precio = "Precio normal"

        total = cantidad * precio_saco

        # Lógica despacho
        if cantidad >= 12:
            despacho = "Despacho a domicilio GRATIS dentro de Coyhaique"
        else:
            despacho = "Retiro en sucursal Coyhaique (Lautaro #257)"

        mensaje = (
            f"Hola 👋, quiero cotizar pellet en Coyhaique.\n\n"
            f"🔥 Pellet certificado – saco 15 kg\n"
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

    except Exception as e:
        return jsonify({
            "error": "Error interno en el servidor",
            "detalle": str(e)
        }), 500


if __name__ == "__main__":
    app.run()
