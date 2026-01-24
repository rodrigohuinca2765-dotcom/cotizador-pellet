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
# CLIENTE OPENAI
# =========================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =========================
# APP
# =========================
app = FastAPI()

# =========================
# MODELO DE ENTRADA
# =========================
class ConsultaIA(BaseModel):
    mensaje: str

# =========================
# HOME (SIN IA)
# =========================
@app.get("/")
def home():
    return "Cotizador IA Ecomas activo 🤖🔥"

# =========================
# IA COTIZADOR (FINAL)
# =========================
@app.post("/ia-cotizar")
def ia_cotizar(data: ConsultaIA):

    # -------- PROMPT DE EXTRACCIÓN --------
    prompt_extraccion = f"""
Eres un asistente de extracción de datos comerciales.

A partir del mensaje del cliente, devuelve EXCLUSIVAMENTE
un JSON válido con esta estructura:

{{
  "cantidad": <numero_entero>
}}

Reglas:
- Si el cliente dice "como 70", "aprox 70", "70 o 75", usa 70
- Si dice un rango, usa el menor
- Si no menciona cantidad, usa 0
- No escribas texto fuera del JSON
- No agregues explicaciones

Mensaje del cliente:
\"\"\"{data.mensaje}\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un extractor de números."},
            {"role": "user", "content": prompt_extraccion}
        ],
        temperature=0
    )

    datos = json.loads(response.choices[0].message.content)
    cantidad = int(datos.get("cantidad", 0))

    # -------- LÓGICA DE NEGOCIO (CONTROLADA) --------
    if cantidad >= 60:
        precio_saco = PRECIO_PROMO
        tipo_precio = "Precio promoción"
    else:
        precio_saco = PRECIO_NORMAL
        tipo_precio = "Precio normal"

    total = cantidad * precio_saco

    # -------- MENSAJE COMERCIAL FINAL --------
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
