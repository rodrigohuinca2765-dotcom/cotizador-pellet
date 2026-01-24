from fastapi import FastAPI
from pydantic import BaseModel
import os
import json
from openai import OpenAI

# =========================
# CONFIGURACIÓN ECOMAS
# =========================
SUCURSAL = "Coyhaique"
DIRECCION = "Lautaro #257"
PRECIO_PROMO = 4240      # Desde 60 sacos
PRECIO_NORMAL = 4990    # Menos de 60 sacos

# =========================
# OPENAI CLIENT
# =========================
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# =========================
# APP FASTAPI
# =========================
app = FastAPI(
    title="Cotizador IA Ecomas",
    version="1.0"
)

# =========================
# MODELO DE ENTRADA
# =========================
class ConsultaIA(BaseModel):
    mensaje: str

# =========================
# HOME (TEST RENDER)
# =========================
@app.get("/")
def home():
    return {"status": "Cotizador IA Ecomas activo 🤖🔥"}

# =========================
# IA COTIZADOR (RUTA CLAVE)
# =========================
@app.post("/ia-cotizar")
def ia_cotizar(data: ConsultaIA):

    prompt = f"""
Extrae SOLO la cantidad de sacos desde el mensaje del cliente.
Devuelve EXCLUSIVAMENTE un JSON válido.

Formato EXACTO:
{{
  "cantidad": <numero_entero>
}}

Reglas:
- "como 70", "aprox 70" → 70
- Rangos → usar el menor
- Si no hay número → 0
- No escribas texto fuera del JSON

Mensaje:
\"\"\"{data.mensaje}\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un extractor de números comerciales."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    datos = json.loads(response.choices[0].message.content)
    cantidad = int(datos.get("cantidad", 0))

    # =========================
    # LÓGICA COMERCIAL
    # =========================
    if cantidad >= 60:
        precio_saco = PRECIO_PROMO
        tipo_precio = "Precio promoción"
    else:
        precio_saco = PRECIO_NORMAL
        tipo_precio = "Precio normal"

    total = cantidad * precio_saco

    mensaje_final = f"""
Hola 👋, quiero cotizar pellet en {SUCURSAL}.

🔥 Pellet certificado – saco 15 kg
📦 Cantidad solicitada: {cantidad} sacos
💰 Precio por saco: ${precio_saco}
🧾 Total estimado: ${total}

📍 Retiro en sucursal {SUCURSAL}
📌 Dirección: {DIRECCION}

🔖 {tipo_precio}
""".strip()

    return {
        "cantidad": cantidad,
        "precio_saco": precio_saco,
        "total": total,
        "mensaje": mensaje_final
    }
