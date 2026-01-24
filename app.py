from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI

# =========================
# CONFIG
# =========================
SUCURSAL = "Coyhaique"
DIRECCION = "Lautaro #257"
PRECIO_PROMO = 4240
PRECIO_NORMAL = 4990

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
# IA COTIZADOR
# =========================
@app.post("/ia-cotizar")
def ia_cotizar(data: ConsultaIA):

    prompt = f"""
Eres un asistente comercial de Ecomas (pellet).

Tu tarea es:
1. Interpretar el mensaje del cliente.
2. Detectar cantidad de sacos (si no está clara, estima).
3. Aplicar precio:
   - {PRECIO_PROMO} CLP por saco si son 60 o más
   - {PRECIO_NORMAL} CLP por saco si son menos de 60
4. Asumir sucursal: {SUCURSAL}
5. Armar un mensaje comercial listo para enviar por WhatsApp.

Mensaje del cliente:
\"\"\"{data.mensaje}\"\"\"

Devuelve SOLO el mensaje final, sin explicaciones técnicas.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un vendedor experto de pellet en Chile."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    mensaje_final = response.choices[0].message.content.strip()

    return {
        "respuesta": mensaje_final,
        "whatsapp": f"https://wa.me/?text={mensaje_final}"
    }
