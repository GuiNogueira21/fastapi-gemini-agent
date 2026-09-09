from google import genai
from google.genai import types
from src.ai.base import AIPlatform

class Gemini(AIPlatform):
    def __init__ (self, api_key: str, system_prompt: str = None):
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.client = genai.Client(api_key=api_key)


    def chat(self, prompt: str) -> str:
        config = None
        if self.system_prompt:
            config = types.GenerateContentConfig(
                system_instruction=self.system_prompt
            )

        response = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config= config,
        )

        return response.text