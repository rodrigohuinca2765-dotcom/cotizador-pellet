import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)  # Permite pruebas desde navegador / Hoppscotch, etc.

# --- OpenAI (IA para reformular texto) ---
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def reformular_con_ia(mensaje_base: str) -> str:
    """
    Usa OpenAI solo para mejorar el texto (tono comercial, claridad).
    Si no hay API key o falla algo, devuelve el mensaje original.
    """
    if not client:
        return mensaje_base

    try:
        resp = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "developer",
                    "content": (
                        "Eres un asistente comercial de Ecomas (Coyhaique). "
                        "Reformula el mensaje de cotización para que sea claro, cordial y profesional. "
                        "NO cambies números, precios, condiciones, dirección ni reglas. "
                        "Mantén emojis moderados y formato fácil de leer."
                    ),
                },
                {"role": "user", "content": mensaje_base},
            ],
        )
        # output_text es la salida final en texto
        texto = (resp.output_text or "").strip()
        return texto if texto else mensaje_base

    except Exception:
        return mensaje_base


# --- Rutas ---
@app.route("/", methods=["GET"])
def home():
    return "Cotizador de Pellet activo 🔥"


@app.route("/cotizar", methods=["POST"])
def cotizar():
    data = request.get_json() or {}
    cantidad = int(data.get("cantidad", 0))

    if cantidad <= 0:
        return jsonify({"error": "La cantidad debe ser mayor a 0"}), 400

    # Precios
    precio_normal = 4990
    precio_promo = 4240

    # Regla de precio
    if cantidad >= 60:
        precio_saco = precio_promo
        tipo_precio = "Precio PROMOCIÓN aplicado (desde 60 sacos)"
    else:
        precio_saco = precio_normal
        tipo_precio = "Precio normal (promoción desde 60 sacos)"

    total = cantidad * precio_saco

    # Regla de despacho
    if cantidad >= 12:
        despacho = "Despacho a domicilio GRATIS dentro de Coyhaique"
    else:
        despacho = "Retiro en sucursal Coyhaique (Lautaro #257)"

    # Mensaje base (reglas)
    mensaje_base = (
        "Hola 👋, quiero cotizar pellet en Coyhaique.\n\n"
        "🔥 Pellet certificado – saco 15 kg\n"
        f"📦 Cantidad solicitada: {cantidad} sacos\n"
        f"💰 Precio por saco: ${precio_saco:,}\n"
        f"🧾 Total estimado: ${total:,}\n\n"
        f"🚚 {despacho}\n"
        f"ℹ️ {tipo_precio}\n"
        "\n"
        "¿Me ayudas con disponibilidad y coordinación?"
    )

    # IA (solo reformula el texto)
    mensaje_final = reformular_con_ia(mensaje_base)

    return jsonify({
        "cantidad": cantidad,
        "precio_saco": precio_saco,
        "total": total,
        "tipo_precio": tipo_precio,
        "despacho": despacho,
        "mensaje": mensaje_final
    })
