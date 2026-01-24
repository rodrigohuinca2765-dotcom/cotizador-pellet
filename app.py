from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI(
    title="Cotizador Pellet Ecomas",
    version="1.0"
)

# ---------- MODELO ----------
class ChatRequest(BaseModel):
    mensaje: str

# ---------- UTILIDAD ----------
def extraer_cantidad(texto: str) -> int:
    match = re.search(r"\d+", texto)
    return int(match.group()) if match else 0

# ---------- RUTA RAÍZ ----------
@app.get("/")
def home():
    return {
        "status": "Cotizador de Pellet activo 🔥",
        "endpoints": ["/chat", "/cotizar"]
    }

# ---------- CHAT / AGENTE ----------
@app.post("/chat")
def chat(request: ChatRequest):
    texto = request.mensaje.lower()
    cantidad = extraer_cantidad(texto)

    # Si no indica cantidad → agente pregunta
    if cantidad == 0:
        return {
            "mensaje": (
                "Hola 👋 soy tu asesor Ecomas.\n\n"
                "Para ayudarte con la cotización necesito saber:\n"
                "👉 ¿Cuántos sacos de pellet necesitas?\n\n"
                "Ejemplo: *Necesito 70 sacos*"
            )
        }

    # Lógica de precios
    if cantidad >= 60:
        precio = 4240
        tipo = "PROMOCIÓN"
    else:
        precio = 4990
        tipo = "normal"

    total = cantidad * precio

    mensaje = (
        f"Perfecto 👍 aquí está tu cotización:\n\n"
        f"🔥 Pellet certificado – saco 15 kg\n"
        f"📦 Cantidad solicitada: {cantidad} sacos\n"
        f"💰 Precio por saco: ${precio:,}\n"
        f"🧾 Total estimado: ${total:,}\n\n"
        f"📍 Retiro en sucursal Coyhaique\n"
        f"📌 Dirección: Lautaro #257\n\n"
        f"🏷️ Precio {tipo}\n\n"
        f"¿Deseas continuar con el pedido o necesitas ajustar la cantidad?"
    )

    return {"mensaje": mensaje}

# ---------- COTIZAR DIRECTO ----------
@app.post("/cotizar")
def cotizar(request: ChatRequest):
    return chat(request)
