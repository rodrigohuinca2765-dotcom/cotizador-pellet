from fastapi import FastAPI, Body
from pydantic import BaseModel
import re

app = FastAPI(
    title="Cotizador Pellet Ecomas",
    description="API de cotización inteligente para Pellet en Coyhaique",
    version="1.0.0"
)

# ---------- MODELO ----------
class IARequest(BaseModel):
    mensaje: str

# ---------- UTILIDAD ----------
def extraer_cantidad(texto: str) -> int:
    match = re.search(r"\d+", texto)
    return int(match.group()) if match else 0

# ---------- RUTA RAÍZ ----------
@app.get("/")
def home():
    return {"status": "Cotizador de Pellet activo 🔥"}

# ---------- IA COTIZADOR ----------
@app.post("/ia-cotizar")
def ia_cotizar(data: IARequest):
    cantidad = extraer_cantidad(data.mensaje)

    if cantidad >= 60:
        precio_saco = 4240
        tipo_precio = "Precio PROMOCIÓN"
    else:
        precio_saco = 4990
        tipo_precio = "Precio normal"

    total = cantidad * precio_saco

    mensaje = f"""
Hola 👋, quiero cotizar pellet en Coyhaique.

🔥 Pellet certificado – saco 15 kg
📦 Cantidad solicitada: {cantidad} sacos
💰 Precio por saco: ${precio_saco:,}
🧾 Total estimado: ${total:,}

📍 Retiro en sucursal Coyhaique
📌 Dirección: Lautaro #257

🔖 {tipo_precio}
""".strip()

    return {
        "cantidad": cantidad,
        "precio_saco": precio_saco,
        "tipo_precio": tipo_precio,
        "total": total,
        "mensaje": mensaje
    }
