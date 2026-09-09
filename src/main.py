import os
from fastapi import FastAPI
from pydantic import BaseModel

#--- App Initialization---
app = FastAPI()

#=== Pydantic Models---
class ChatRequest(BaseModel):
    prompt: str # We expect a JSON body like {"prompt": "..."}

class ChatResponse(BaseModel):
    response: str # We'll return a JSON body like {"response": "..."}

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.post("/chat", response_model = ChatResponse)
async def chat (request: ChatResponse):
    #TODO: Implement AI integration
    response_text = "..."
    return ChatResponse(response= response_text)