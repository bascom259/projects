from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from google import genai

app = FastAPI()

# HTML templates folder
templates = Jinja2Templates(directory="templates")

# Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ---------------- HOME PAGE ----------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# ---------------- CHAT API ----------------
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=req.message
    )

    return {"reply": response.text}
