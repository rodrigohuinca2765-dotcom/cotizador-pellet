from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import re
import csv
import os
from openai import OpenAI

# ===============================
# CONFIG
# ===============================
PRECIO_NORMAL = 4990
PRECIO_PROMO = 4240
MIN_PROMO = 60
SUCURSAL = "Coyhaique (Lautaro #257)"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(
    title="Cotizador Pellet Ecomas 🔥",
    description="Cotizador inteligente con IA + QR + WhatsApp",
    version="1.0"
)

# ===============================
# MODELO INPUT
# ===============================
class Consulta(BaseModel):
    mensaje: str

# ===============================
# FUNCIONES
# ===============================
def extraer_cantidad(texto: str) -> int:
    numeros = re.findall(r"\d+", texto)
    return int(numeros[0]) if numeros else 0

def guardar_csv(cantidad, precio, total, tipo):
    existe = os.path.exists("cotizaciones.csv")
    with open("cotizaciones.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow([
                "fecha_hora", "cantidad", "precio_unitario",
                "total", "tipo_precio", "sucursal"
            ])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            cantidad, precio, total, tipo, SUCURSAL
        ])

# ===============================
# ENDPOINT RAÍZ (TEST)
# ===============================
@app.get("/")
def home():
    return {"status": "Cotizador activo 🔥"}

# ===============================
# ENDPOINT IA
# ===============================
@app.post("/ia-cotizar")
def cotizar(data: Consulta):
    texto = data.mensaje
    cantidad = extraer_cantidad(texto)

    if cantidad >= MIN_PROMO:
        precio = PRECIO_PROMO
        tipo = "Precio promoción"
    else:
        precio = PRECIO_NORMAL
        tipo = "Precio normal"

    total = cantidad * precio

    guardar_csv(cantidad, precio, total, tipo)

    mensaje_final = (
        f"Hola 👋, quiero cotizar pellet en Coyhaique.\n\n"
        f"🔥 Pellet certificado – saco 15 kg\n"
        f"📦 Cantidad solicitada: {cantidad} sacos\n"
        f"💰 Precio por saco: ${precio:,}\n"
        f"🧾 Total estimado: ${total:,}\n\n"
        f"📍 Retiro en sucursal {SUCURSAL}\n"
        f"ℹ️ {tipo}"
    )

    return {
        "cantidad": cantidad,
        "precio_saco": precio,
        "total": total,
        "tipo_precio": tipo,
        "mensaje": mensaje_final
    }
