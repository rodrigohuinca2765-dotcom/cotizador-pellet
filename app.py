from fastapi import FastAPI
from pydantic import BaseModel
import re
import os
from openai import OpenAI

# ---------- APP ----------
app = FastAPI(
    title="Cotizador Pellet Ecomas",
    description="API de cotización inteligente con IA",
    version="2.0"
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------- MODELO ----------
class IARequest(BaseModel):
    mensaje: str

# ---------- UTIL ----------
def extraer_cantidad(texto: str) -> int:
    match = re.search(r"\d+", texto)
    return int(match.group()) if match else 0

# ---------- HOME ----------
@app.get("/")
def home():
    return {"status": "Cotizador de Pellet activo 🔥"}

# ---------- IA COTIZADOR ----------
@app.post("/ia-cotizar")
def ia_cotizar(data: IARequest):
    texto = data.mensaje
    sacos = extraer_cantidad(texto)

    if sacos >= 60:
        precio = 4240
        tipo = "Precio PROMOCIÓN"
    else:
        precio = 4990
        tipo = "Precio normal"

    total = sacos * precio

    prompt = f"""
Eres un asistente comercial de Ecomas.
Genera una respuesta clara y cordial con estos datos:

- Producto: Pellet certificado, saco 15 kg
- Cantidad: {sacos}
- Precio por saco: ${precio}
- Total: ${total}
- Retiro: Sucursal Coyhaique, Lautaro #257
- Tipo de precio: {tipo}
"""

    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "cantidad": sacos,
        "precio_saco": precio,
        "tipo_precio": tipo,
        "total": total,
        "mensaje": respuesta.choices[0].message.content
    }
