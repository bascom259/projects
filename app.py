from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
import google.generativeai as genai
import os

app = FastAPI()

# Load API key from environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

class Chat(BaseModel):
    message: str

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/chat")
def chat(data: Chat):

    prompt = f"""
You are a friendly AI companion who talks casually and supportively.

User: {data.message}
Assistant:
"""

    response = model.generate_content(prompt)

    return {"reply": response.text}