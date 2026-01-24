from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Cotizador de Pellet activo 🔥"

# -------------------------------
# PASO A + B: COTIZADOR
# -------------------------------
@app.route("/cotizar", methods=["POST"])
def cotizar():
    data = request.get_json()
    cantidad = int(data.get("cantidad", 0))

    precio_normal = 4990
    precio_promo = 4290

    if cantidad >= 60:
        precio = precio_promo
        tipo_precio = "Precio PROMOCIÓN aplicado"
    else:
        precio = precio_normal
        tipo_precio = "Precio normal"

    total = cantidad * precio

    if cantidad >= 12:
        despacho = "Despacho a domicilio GRATIS dentro de Coyhaique"
    else:
        despacho = "Retiro en sucursal Coyhaique (Lautaro #257)"

    if cantidad < 12:
        sugerencia_ia = (
            "💡 Desde 12 sacos obtienes despacho a domicilio GRATIS dentro de Coyhaique."
        )
    elif cantidad < 60:
        sugerencia_ia = (
            f"💡 Si llegas a 60 sacos accedes a PRECIO PROMOCIÓN por saco."
        )
    else:
        sugerencia_ia = (
            "✅ Estás aprovechando el mejor precio disponible."
        )

    mensaje = (
        "Hola 👋, quiero cotizar pellet en Coyhaique.\n\n"
        f"📦 Cantidad: {cantidad} sacos (15 kg)\n"
        f"💰 Precio por saco: ${precio:,}\n"
        f"🧾 Total: ${total:,}\n\n"
        f"🚚 {despacho}\n"
        f"🤖 {sugerencia_ia}"
    )

    return jsonify({
        "cantidad": cantidad,
        "precio_saco": precio,
        "tipo_precio": tipo_precio,
        "total": total,
        "despacho": despacho,
        "mensaje": mensaje
    })


# -------------------------------
# PASO C: IA CONVERSACIONAL
# -------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    texto = data.get("mensaje", "").lower()

    if "precio" in texto or "valor" in texto:
        respuesta = (
            "💰 El valor por saco es $4.990.\n"
            "🔥 Desde 60 sacos accedes a precio PROMOCIÓN de $4.290."
        )

    elif "despacho" in texto or "envío" in texto:
        respuesta = (
            "🚚 Desde 12 sacos el despacho es GRATIS dentro de Coyhaique.\n"
            "📍 Menos de 12 sacos es retiro en sucursal."
        )

    elif "cuantos" in texto or "recomiendas" in texto:
        respuesta = (
            "🏠 Para una vivienda promedio recomendamos entre 20 y 40 sacos.\n"
            "🔥 Para el mejor precio, 60 sacos es la opción ideal."
        )

    elif "hola" in texto:
        respuesta = (
            "Hola 👋 Soy el asistente de Ecomas.\n"
            "Puedo ayudarte a cotizar, recomendar cantidad o resolver dudas."
        )

    else:
        respuesta = (
            "🤖 Puedo ayudarte con precios, despacho o recomendación de cantidad.\n"
            "¿Qué te gustaría saber?"
        )

    return jsonify({
        "respuesta": respuesta
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
