import os
import re
from typing import List, Optional, Dict, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from openai import OpenAI


# =============================
# CONFIG
# =============================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()

# URLs permitidas (GitHub Pages + tu backend)
ALLOWED_ORIGINS = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "https://rodrigohuinca2765-dotcom.github.io",
    "https://rodrigohuinca2765-dotcom.github.io/cotizador-pellet",
    "https://rodrigohuinca2765-dotcom.github.io/cotizador-pellet/",
]

WHATSAPP_NUMBER = "56991422163"  # Rodrigo

# Reglas de precios
PRECIO_NORMAL = 4990
PRECIO_PROMO = 4240
MIN_PROMO = 60

SUCURSAL = "Sucursal Coyhaique"
DIRECCION = "Lautaro #257"


# =============================
# APP
# =============================
app = FastAPI(
    title="Cotizador Pellet Ecomas",
    description="API + Agente de ventas para cotización de pellet en Coyhaique",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================
# MODELOS
# =============================
class ChatMessage(BaseModel):
    role: str  # "user" o "assistant"
    content: str


class ChatRequest(BaseModel):
    mensaje: str
    history: Optional[List[ChatMessage]] = None


# =============================
# UTILIDADES
# =============================
def extraer_cantidad(texto: str) -> Optional[int]:
    """
    Extrae el primer número entero encontrado en el texto.
    """
    if not texto:
        return None
    m = re.search(r"\b(\d{1,4})\b", texto)
    if not m:
        return None
    try:
        return int(m.group(1))
    except:
        return None


def calcular_precio(cantidad: int) -> Dict[str, Any]:
    """
    Retorna precio por saco, tipo de precio y total.
    """
    if cantidad >= MIN_PROMO:
        precio = PRECIO_PROMO
        tipo = "Precio PROMOCIÓN"
    else:
        precio = PRECIO_NORMAL
        tipo = "Precio normal"

    total = cantidad * precio
    return {"precio_saco": precio, "tipo_precio": tipo, "total": total}


def build_whatsapp_url(texto: str) -> str:
    # Encoding simple (espacios y saltos)
    from urllib.parse import quote

    return f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(texto)}"


def formatear_cotizacion(cantidad: int, precio_saco: int, tipo_precio: str, total: int) -> str:
    return (
        "Hola 👋, quiero cotizar pellet en Coyhaique.\n\n"
        "🔥 Pellet certificado – saco 15 kg\n"
        f"📦 Cantidad solicitada: {cantidad} sacos\n"
        f"💰 Precio por saco: ${precio_saco:,}".replace(",", ".") + "\n"
        f"🧾 Total estimado: ${total:,}".replace(",", ".") + "\n\n"
        f"📍 Retiro en {SUCURSAL}\n"
        f"📌 Dirección: {DIRECCION}\n\n"
        f"✅ {tipo_precio}"
    )


def openai_required() -> None:
    if not OPENAI_API_KEY:
        raise RuntimeError("Falta OPENAI_API_KEY en variables de entorno (Render).")


# =============================
# RUTAS
# =============================
@app.get("/")
def home():
    return {"status": "Cotizador de Pellet activo 🔥", "endpoints": ["/chat", "/cotizar"]}


@app.post("/cotizar")
def cotizar(payload: Dict[str, Any]):
    """
    Endpoint simple: recibe {"mensaje": "..."} y responde cotización (sin IA).
    """
    texto = payload.get("mensaje", "")
    cantidad = extraer_cantidad(texto) or 0

    if cantidad <= 0:
        return {
            "ok": True,
            "cantidad": 0,
            "mensaje": (
                "👋 Hola, para cotizar necesito que me digas cuántos sacos quieres.\n"
                "Ejemplo: “Necesito 70 sacos de pellet para Coyhaique”."
            ),
            "ready_for_whatsapp": False,
        }

    calc = calcular_precio(cantidad)
    mensaje = formatear_cotizacion(cantidad, calc["precio_saco"], calc["tipo_precio"], calc["total"])
    return {
        "ok": True,
        "cantidad": cantidad,
        "precio_saco": calc["precio_saco"],
        "tipo_precio": calc["tipo_precio"],
        "total": calc["total"],
        "mensaje": mensaje,
        "ready_for_whatsapp": True,
        "whatsapp_url": build_whatsapp_url(mensaje),
    }


@app.post("/chat")
def chat(req: ChatRequest):
    """
    Chat con IA tipo agente de ventas.
    - Si el cliente NO da cantidad -> la IA pregunta.
    - Si el cliente da cantidad -> cotiza con regla promo>=60 y ofrece WhatsApp.
    """
    openai_required()
    client = OpenAI(api_key=OPENAI_API_KEY)

    user_text = (req.mensaje or "").strip()
    history = req.history or []

    # Intentamos extraer cantidad desde el mensaje actual
    cantidad = extraer_cantidad(user_text)

    system_prompt = f"""
Eres un agente de ventas profesional de Ecomas Coyhaique (Chile).
Tu objetivo es cerrar ventas de pellet, con respuestas breves y claras.

REGLAS (OBLIGATORIAS):
- Solo cotizas Pellet certificado, saco 15 kg.
- Lugar: {SUCURSAL}. Dirección: {DIRECCION}.
- No inventes despacho ni otros productos.
- Precios:
  - PROMOCIÓN: ${PRECIO_PROMO} por saco si cantidad >= {MIN_PROMO}
  - NORMAL: ${PRECIO_NORMAL} por saco si cantidad < {MIN_PROMO}
- Si el cliente NO dice cantidad, debes preguntar: “¿Cuántos sacos necesitas aproximadamente?”
- Cuando ya tengas cantidad, entregas cotización y preguntas si desea coordinar por WhatsApp.
- Mantén tono amable, vendedor, directo.

FORMATO DE SALIDA: Responde SIEMPRE en JSON válido con estas claves:
- reply: string (respuesta que verá el cliente)
- quantity: number|null
- ready_for_quote: boolean
"""

    # Armamos mensajes para OpenAI (incluye historial)
    msgs = [{"role": "system", "content": system_prompt}]
    for m in history[-10:]:
        # Sanitiza roles
        role = "assistant" if m.role == "assistant" else "user"
        msgs.append({"role": role, "content": m.content})
    msgs.append({"role": "user", "content": user_text})

    # Si ya hay cantidad, NO necesitamos que la IA calcule números: lo hacemos nosotros con regla fija.
    # Igual le pedimos que redacte “como vendedor” y que confirme cierre.
    if cantidad is not None and cantidad > 0:
        calc = calcular_precio(cantidad)
        cotizacion_texto = formatear_cotizacion(cantidad, calc["precio_saco"], calc["tipo_precio"], calc["total"])

        # Pedimos a la IA que redacte un cierre bonito (sin cambiar números)
        assistant_prompt = f"""
El cliente pidió {cantidad} sacos.

Estos son los datos oficiales (NO los cambies):
- Precio por saco: {calc["precio_saco"]}
- Total: {calc["total"]}
- Tipo: {calc["tipo_precio"]}
- Retiro: {SUCURSAL}, {DIRECCION}

Redacta una respuesta breve y vendedora, y termina preguntando si coordinamos por WhatsApp.
Devuelve el JSON con:
quantity={cantidad} y ready_for_quote=true.
"""

        msgs.append({"role": "user", "content": assistant_prompt})

        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=msgs,
            temperature=0.3,
        )

        content = resp.choices[0].message.content or ""

        # Intentamos extraer JSON (por si la IA mete texto extra)
        json_text = content.strip()
        # fallback básico
        if not json_text.startswith("{"):
            json_text = '{"reply":"Perfecto, ¿cuántos sacos necesitas aproximadamente?","quantity":null,"ready_for_quote":false}'

        # Construimos respuesta final con cotización + botón WA
        reply = None
        try:
            import json
            data = json.loads(json_text)
            reply = data.get("reply")
        except:
            reply = "Perfecto 👍"

        # Adjuntamos cotización oficial abajo (siempre)
        full_reply = f"{reply}\n\n{cotizacion_texto}\n\n¿Te parece si lo coordinamos por WhatsApp?"

        return {
            "ok": True,
            "agent_reply": full_reply,
            "cantidad": cantidad,
            "precio_saco": calc["precio_saco"],
            "tipo_precio": calc["tipo_precio"],
            "total": calc["total"],
            "ready_for_whatsapp": True,
            "whatsapp_url": build_whatsapp_url(cotizacion_texto),
        }

    # Si NO hay cantidad, dejamos que la IA pregunte
    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=msgs,
        temperature=0.4,
    )

    content = resp.choices[0].message.content or ""
    json_text = content.strip()
    if not json_text.startswith("{"):
        json_text = '{"reply":"👋 ¡Hola! Para cotizar necesito saber la cantidad. ¿Cuántos sacos necesitas aproximadamente?","quantity":null,"ready_for_quote":false}'

    reply = "👋 ¡Hola! ¿Cuántos sacos necesitas aproximadamente?"
    qty = None
    ready = False
    try:
        import json
        data = json.loads(json_text)
        reply = data.get("reply", reply)
        qty = data.get("quantity", None)
        ready = bool(data.get("ready_for_quote", False))
    except:
        pass

    return {
        "ok": True,
        "agent_reply": reply,
        "cantidad": qty,
        "ready_for_whatsapp": False,
    }
