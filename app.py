from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os

from google import genai

# ---------------- APP ----------------
app = FastAPI()

# Static + Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ---------------- GEMINI ----------------
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ---------------- ROUTES ----------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(data: ChatRequest):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=data.message
    )

    return {"reply": response.text}
