from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from google import genai
import os

app = FastAPI()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data["message"]

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
    )

    return JSONResponse({"reply": response.text})
