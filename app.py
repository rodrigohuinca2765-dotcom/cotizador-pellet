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
    precio_promo = 4290  # dejamos este valor como pediste

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
        despacho = "Despacho a domicilio GRATIS dentro de Coyhaique"
    else:
        despacho = "Retiro en sucursal Coyhaique (Lautaro #257)"

    # 🧠 IA – sugerencias inteligentes
    if cantidad < 12:
        sugerencia_ia = (
            "💡 Sugerencia IA: Desde 12 sacos obtienes despacho a domicilio GRATIS "
            "dentro de Coyhaique. ¿Te gustaría ajustar tu compra?"
        )
    elif 12 <= cantidad < 60:
        faltan = 60 - cantidad
        sugerencia_ia = (
            f"💡 Sugerencia IA: Si agregas {faltan} sacos más accedes a "
            "PRECIO PROMOCIÓN por saco y optimizas tu compra."
        )
    else:
        sugerencia_ia = (
            "✅ Excelente elección. Estás aprovechando el mejor precio disponible "
            "con despacho incluido."
        )

    # Mensaje comercial
    mensaje = (
        "Hola 👋, quiero cotizar pellet en Coyhaique.\n\n"
        "🔥 Pellet certificado – saco 15 kg\n"
        f"📦 Cantidad solicitada: {cantidad} sacos\n"
        f"💰 Precio por saco: ${precio:,}\n"
        f"🧾 Total estimado: ${total:,}\n\n"
        f"🚚 {despacho}\n"
        f"🤖 {sugerencia_ia}"
    )

    return jsonify({
        "cantidad": cantidad,
        "precio_saco": precio,
        "tipo_precio": tipo_precio,
        "total": total,
        "despacho": despacho,
        "sugerencia_ia": sugerencia_ia,
        "mensaje": mensaje
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
