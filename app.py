import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PRECIO_NORMAL = 4990
PRECIO_PROMO = 4240
MIN_PROMO = 60

app = FastAPI(title="Agente de Ventas Pellet Ecomas")

class IARequest(BaseModel):
    mensaje: str
    contexto: list | None = []

@app.get("/")
def home():
    return {"status": "Agente de ventas Ecomas activo 🔥"}

@app.post("/ia-cotizar")
def ia_cotizar(data: IARequest):

    system_prompt = f"""
Eres un AGENTE DE VENTAS de Ecomas Pellet Coyhaique.

Reglas:
- Conversa con el cliente de forma natural.
- Si NO sabes la cantidad, pregunta cuántos sacos necesita.
- Si sabes la cantidad pero no la ciudad, pregunta la ciudad.
- Cuando tengas cantidad y ciudad, entrega la cotización completa.
- Aplica precio promoción si cantidad >= {MIN_PROMO}.
- NO inventes datos.
- NO uses emojis en exceso.
- Responde siempre en español.
"""

    messages = [{"role": "system", "content": system_prompt}]

    if data.contexto:
        messages.extend(data.contexto)

    messages.append({"role": "user", "content": data.mensaje})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3
    )

    respuesta = response.choices[0].message.content

    return {
        "mensaje": respuesta,
        "nuevo_contexto": messages + [{"role": "assistant", "content": respuesta}]
    }
