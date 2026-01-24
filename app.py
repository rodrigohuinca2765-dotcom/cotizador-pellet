from fastapi import FastAPI
from pydantic import BaseModel
import os
import openai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# ---------- MODELOS ----------
class Consulta(BaseModel):
    cantidad: int | None = None
    mensaje: str | None = None


# ---------- FUNCIÓN IA ----------
def responder_con_ia(texto_usuario: str):
    prompt = f"""
Eres un asistente comercial de Ecomas Coyhaique.
Respondes de forma clara, amable y profesional.

Información clave:
- Pellet certificado saco 15 kg
- Precio normal: $4.990
- Precio promoción: $4.240 desde 60 sacos
- Desde 12 sacos: despacho GRATIS dentro de Coyhaique
- Menos de 12 sacos: retiro en sucursal Lautaro #257

Pregunta del cliente:
"{texto_usuario}"
"""

    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return respuesta.choices[0].message.content


# ---------- ENDPOINT ----------
@app.post("/cotizar")
def cotizar(data: Consulta):

    # 🧠 SI VIENE MENSAJE → IA
    if data.mensaje:
        respuesta_ia = responder_con_ia(data.mensaje)
        return {
            "tipo": "ia",
            "respuesta": respuesta_ia
        }

    # 🧮 SI VIENE CANTIDAD → REGLAS
    cantidad = data.cantidad or 0

    if cantidad >= 60:
        precio = 4240
        tipo_precio = "Precio PROMOCIÓN aplicado"
    else:
        precio = 4990
        tipo_precio = "Precio normal"

    total = cantidad * precio

    if cantidad >= 12:
        despacho = "Despacho a domicilio GRATIS dentro de Coyhaique"
    else:
        despacho = "Retiro en sucursal Coyhaique (Lautaro #257)"

    mensaje = f"""
🔥 Cotización Pellet Coyhaique

📦 Cantidad: {cantidad} sacos (15 kg c/u)
💰 Precio por saco: ${precio}
🧾 Total estimado: ${total}

🚚 {despacho}
ℹ️ {tipo_precio}
"""

    return {
        "cantidad": cantidad,
        "precio_saco": precio,
        "total": total,
        "despacho": despacho,
        "tipo_precio": tipo_precio,
        "mensaje": mensaje
    }
