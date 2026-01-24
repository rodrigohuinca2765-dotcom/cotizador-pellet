from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

app = FastAPI(
    title="Cotizador Pellet Ecomas",
    description="API de cotización inteligente para Pellet en Coyhaique",
    version="1.0.0"
)

# 🔥 CORS (CLAVE PARA GITHUB PAGES)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # luego lo cerramos, hoy lo dejamos abierto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
def cotizar(data: IARequest):
    texto = data.mensaje.lower()
    cantidad = extraer_cantidad(texto)

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
        f"👉 {tipo_precio}"
    )

    return {
        "cantidad": cantidad,
        "precio_saco": precio_saco,
        "tipo_precio": tipo_precio,
        "total": total,
        "mensaje": mensaje
    }
