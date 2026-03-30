from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os

from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# Tell FastAPI where HTML files exist
templates = Jinja2Templates(directory="templates")


# ---------- Serve Website ----------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# ---------- Chat API ----------
class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(req: ChatRequest):

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"You are a friendly AI companion.\nUser: {req.message}"
    )

    return {"reply": response.text}
