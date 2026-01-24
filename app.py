from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# Cliente OpenAI (SDK nuevo)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {
        "status": "Cotizador de Pellet activo 🔥",
        "endpoints": ["/chat"]
    }

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        system_prompt = """
Eres un agente de ventas de Ecomas en Coyhaique.
Tu objetivo es ayudar a cotizar pellet de forma clara y amable.

Datos comerciales:
- Pellet certificado saco 15 kg
- Precio normal: $4.990 por saco
- Precio promoción: $4.240 por saco desde 60 sacos
- Retiro en sucursal Coyhaique
- Dirección: Lautaro #257

Reglas:
1. Si el cliente no indica cantidad, pregúntala.
2. Si indica cantidad >= 60, aplica precio promoción.
3. Responde siempre como vendedor humano, cercano y profesional.
4. Termina invitando a continuar la conversación.
"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": req.message}
            ],
            temperature=0.4
        )

        return {
            "reply": response.choices[0].message.content
        }

    except Exception as e:
        return {
            "error": str(e)
        }
