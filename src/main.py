import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from src.ai.gemini import Gemini
from src.auth.throttling import apply_rate_limit


load_dotenv()


def load_system_prompt():
    try:
        with open("src/prompts/system_prompt.md", "r") as f:
            return f.read()
    except FileNotFoundError:
        return None


#--- App Initialization---
app = FastAPI()


system_prompt = load_system_prompt()
gemini_api_key = os.getenv("GEMINI_API_KEY")


if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")


#Create an instance of the AI platform, ready to use
ai_platform = Gemini(api_key = gemini_api_key, system_prompt= system_prompt)


#=== Pydantic Models---
class ChatRequest(BaseModel):
    prompt: str # We expect a JSON body like {"prompt": "..."}


class ChatResponse(BaseModel):
    response: str # We'll return a JSON body like {"response": "..."}


@app.get("/")
async def root():
    return {"message": "API is running"}


@app.post("/chat", response_model = ChatResponse)
async def chat (request: ChatRequest):
    apply_rate_limit("global_unauthenticated_user")
    response_text = ai_platform.chat(request.prompt)
    return ChatResponse(response= response_text)