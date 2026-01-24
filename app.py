import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

# ---------- CONFIG ----------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PRECIO_NORMAL = 4990
PRECIO_PROMO = 4240
MIN_PROMO = 60

# ---------- APP ----------
app = FastAPI(
    title="Cotizador Pellet Ecomas",
    description="Cotizador inteligente con IA",
    version="1.0"
)

class IARequest(BaseModel):
    mensaje: str

# ---------- RUTA RAÍZ ----------
@app.get("/")
def home():
    return {"status": "Cotizador de Pellet activo 🔥"}

# ---------- IA COTIZADOR ----------
@app.post("/ia-cotizar")
def ia_cotizar(data: IARequest):

    prompt = f"""
Eres un asistente comercial de Ecomas Pellet Coyhaique.

Tarea:
1. Detecta cuántos sacos de pellet quiere el cliente.
2. Si no indica cantidad, asume 0.
3. Responde SOLO en JSON con esta estructura:

{{
  "cantidad": numero,
  "mensaje": "mensaje final al cliente"
}}

Mensaje del cliente:
\"{data.mensaje}\"
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    ia_json = eval(response.choices[0].message.content)

    cantidad = int(ia_json.get("cantidad", 0))

    if cantidad >= MIN_PROMO:
        precio = PRECIO_PROMO
        tipo = "Precio PROMOCIÓN"
    else:
        precio = PRECIO_NORMAL
        tipo = "Precio normal"

    total = cantidad * precio

    mensaje_final = (
        f"Hola 👋, quiero cotizar pellet en Coyhaique.\n\n"
        f"🔥 Pellet certificado – saco 15 kg\n"
        f"📦 Cantidad solicitada: {cantidad} sacos\n"
        f"💰 Precio por saco: ${precio:,}\n"
        f"🧾 Total estimado: ${total:,}\n\n"
        f"📍 Retiro en sucursal Coyhaique\n"
        f"📌 Dirección: Lautaro #257\n\n"
        f"👉 {tipo}"
    )

    return {
        "cantidad": cantidad,
        "precio_saco": precio,
        "total": total,
        "mensaje": mensaje_final
    }
