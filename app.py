from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

# ---------- CONFIG ----------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# ---------- APP ----------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- MODELS ----------
class ChatRequest(BaseModel):
    message: str

# ---------- ROUTES ----------
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
Eres un agente de ventas de ECOMAS en Coyhaique.
Tu trabajo es:
- Saludar cordialmente
- Pedir datos si faltan (cantidad, ciudad)
- Cotizar pellet saco 15 kg
- Precio normal: $4.990
- Precio promoción: $4.240 desde 60 sacos
- Retiro en sucursal Coyhaique
- Dirección: Lautaro #257
Habla claro, amable y comercial.
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
