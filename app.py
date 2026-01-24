from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI(
    title="Cotizador Pellet Ecomas",
    description="API con IA para cotización de pellet vía QR, web y WhatsApp",
    version="1.0.0"
)

# -------- MODELO --------
class Consulta(BaseModel):
    mensaje: str


# -------- ENDPOINT SALUD --------
@app.get("/")
def home():
    return {"status": "Cotizador activo 🔥"}


# -------- ENDPOINT IA --------
@app.post("/ia-cotizar")
def ia_cotizar(data: Consulta):

    texto = data.mensaje.lower()

    # Extraer número de sacos
    match = re.search(r"(\d+)", texto)
    cantidad = int(match.group(1)) if match else 0

    # Precios
    PRECIO_PROMO = 4240
    PRECIO_NORMAL = 4990

    if cantidad >= 60:
        precio = PRECIO_PROMO
        tipo = "Precio promoción"
    else:
        precio = PRECIO_NORMAL
        tipo = "Precio normal"

    total = cantidad * precio

    mensaje = (
        "Hola 👋, quiero cotizar pellet en Coyhaique.\n\n"
        "🔥 Pellet certificado – saco 15 kg\n"
        f"📦 Cantidad solicitada: {cantidad} sacos\n"
        f"💰 Precio por saco: ${precio:,}\n"
        f"🧾 Total estimado: ${total:,}\n\n"
        "📍 Retiro en sucursal Coyhaique (Lautaro #257)\n"
        f"ℹ️ {tipo}"
    )

    return {
        "cantidad": cantidad,
        "precio_saco": precio,
        "total": total,
        "tipo_precio": tipo,
        "mensaje": mensaje
    }
