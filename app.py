from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from openai import OpenAI

# =============================
# CONFIGURACIÓN
# =============================
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# =============================
# REGLAS DE NEGOCIO (ECOMAS)
# =============================
PRECIO_NORMAL = 4990
PRECIO_PROMO = 4290
MIN_PROMO = 60

DIRECCION = "Lautaro #257, Coyhaique"
DESPACHO_GRATIS_DESDE = 12

# =============================
# FUNCIÓN COTIZAR
# =============================
def cotizar(cantidad: int):
    if cantidad >= MIN_PROMO:
        precio = PRECIO_PROMO
        tipo = "Precio PROMOCIÓN aplicado"
    else:
        precio = PRECIO_NORMAL
        tipo = "Precio normal"

    total = cantidad * precio

    if cantidad >= DESPACHO_GRATIS_DESDE:
        despacho = "Despacho a domicilio GRATIS dentro de Coyhaique"
    else:
        despacho = f"Retiro en sucursal Coyhaique ({DIRECCION})"

    mensaje = (
        f"🔥 Cotización de Pellet – Coyhaique\n\n"
        f"🪵 Pellet certificado – saco 15 kg\n"
        f"📦 Cantidad: {cantidad} sacos\n"
        f"💰 Precio por saco: ${precio:,}\n"
        f"🧾 Total estimado: ${total:,}\n\n"
        f"🚚 {despacho}\n"
        f"ℹ️ {tipo}"
    )

    return {
        "cantidad": cantidad,
        "precio_saco": precio,
        "tipo_precio": tipo,
        "despacho": despacho,
        "total": total,
        "mensaje": mensaje
    }

# =============================
# IA: INTERPRETAR MENSAJE
# =============================
def interpretar_con_ia(texto_usuario: str):
    prompt = f"""
Eres un asesor de ventas experto de Ecomas en Coyhaique.
Reglas:
- Nunca inventes precios
- Si no hay cantidad, responde informativo
- Si el usuario pregunta por recomendación, explica
- Sé claro, cercano y profesional

Mensaje del cliente:
\"\"\"{texto_usuario}\"\"\"
"""

    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un vendedor experto de pellet."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return respuesta.choices[0].message.content

# =============================
# ENDPOINT PRINCIPAL
# =============================
@app.route("/cotizar", methods=["POST"])
def cotizar_endpoint():
    data = request.json or {}

    # CASO 1: viene cantidad
    if "cantidad" in data:
        try:
            cantidad = int(data["cantidad"])
            return jsonify(cotizar(cantidad))
        except:
            return jsonify({"error": "Cantidad inválida"}), 400

    # CASO 2: viene mensaje (IA)
    if "mensaje" in data:
        texto = data["mensaje"]
        respuesta_ia = interpretar_con_ia(texto)

        return jsonify({
            "mensaje": respuesta_ia,
            "nota": "Respuesta generada por IA"
        })

    return jsonify({"error": "Debes enviar cantidad o mensaje"}), 400

# =============================
# ARRANQUE
# =============================
if __name__ == "__main__":
    app.run(debug=True)
