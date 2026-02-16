import config
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI

class Gemini:
    
    def __init__(self):
        self.model = config.GEMINI_MODEL
        self.client = ChatGoogleGenerativeAI(
            model=self.model,
            api_key=config.GEMINI_API_KEY,
            temperature=0.8,
            max_tokens=500
        )
    
    def generate_response(self, messages: List) -> str:
        try:
            response = self.client.invoke(messages)
            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Sorry, I couldn't generate a response at this time."
    
    def __str__(self):
        return f"Gemini(model={self.model})"
    