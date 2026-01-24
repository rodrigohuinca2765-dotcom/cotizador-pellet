from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

# =========================
# CONFIG
# =========================
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

app = FastAPI()

# =========================
# CORS (OBLIGATORIO)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # GitHub Pages
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# MODELOS
# =========================
class ChatRequest(BaseModel):
    message: str

# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {
        "status": "Cotizador de Pellet activo 🔥",
        "endpoints": ["/chat"]
    }

# =========================
# CHAT OPENAI
# =========================
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un agente de ventas de Ecomas en Coyhaique. "
                        "Vendes pellet certificado en sacos de 15 kg. "
                        "Precio normal: $4.990 por saco. "
                        "Si el cliente compra 60 sacos o más, precio promoción: $4.240 por saco. "
                        "Retiro en sucursal Coyhaique, dirección Lautaro #257. "
                        "Guía la conversación, pregunta cantidad y responde claro y amable."
                    )
                },
                {"role": "user", "content": req.message}
            ],
            temperature=0.4
        )

        return {
            "reply": response.choices[0].message["content"]
        }

    except Exception as e:
        return {
            "error": str(e)
        }
