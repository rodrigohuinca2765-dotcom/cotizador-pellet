from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI(
    title="Cotizador Pellet Ecomas",
    description="API de cotización inteligente para Pellet en Coyhaique",
    version="1.0.0"
)

# 🔥 CORS (ESTO ES LO QUE FALTABA)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción se puede limitar
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IARequest(BaseModel):
    mensaje: str

def extraer_cantidad(texto: str) -> int:
    match = re.search(r"\d+", texto)
    return int(match.group()) if match else 0

@app.get("/")
def home():
    return {"status": "Cotizador de Pellet activo 🔥"}

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

    mensaje = (
        f"Hola 👋, quiero cotizar pellet en Coyhaique.\n\n"
        f"🔥 Pellet certificado – saco 15 kg\n"
        f"📦 Cantidad solicitada: {cantidad} sacos\n"
        f"💰 Precio por saco: ${precio_saco:,}\n"
        f"🧾 Total estimado: ${total:,}\n\n"
        f"📍 Retiro en sucursal Coyhaique\n"
        f"📌 Dirección: Lautaro #257\n\n"
        f"🏷 {tipo_precio}"
    )

    return {
        "cantidad": cantidad,
        "precio_saco": precio_saco,
        "tipo_precio": tipo_precio,
        "total": total,
        "mensaje": mensaje
    }
