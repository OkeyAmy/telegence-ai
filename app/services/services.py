"""
This module contains the AIService class which handles interactions with the AI model.
It includes methods for generating greetings, responses, and email replies.
"""


from typing import List, Optional
import google.generativeai as genai
from fastapi import HTTPException
from app.config import get_settings
from app.templates.templates import MessageType, MESSAGE_TEMPLATES

# services.py
class AIService:
    def __init__(self):
        settings = get_settings()
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    async def greet_user(self, message: str) -> str:
        try:
            greeting = self.model.generate_content(message)
            return greeting.text.strip()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"AI greeting error: {str(e)}")

    async def generate_response(self, message_type: str, user_message: str) -> str:
        try:
            template = self._get_message_template(message_type)
            prompt = template.format(custom_message=user_message)
            response = self.model.generate_content(f"Rewrite the prompt: {prompt} so that it will be email formatted")
            return response.text.strip()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"AI generation error: {str(e)}")

    def _get_message_template(self, message_type: str) -> str:
        try:
            return MESSAGE_TEMPLATES[MessageType(message_type)]
        except ValueError:
            return MESSAGE_TEMPLATES[MessageType.CUSTOM]
        
    async def email_responder(self, email_address: str, email: str, prompt: str, message_type: str) -> str:
        try:
            message_template = self._get_message_template(message_type)
            messages = [
                f'Write a response to this email and sign the email with the name only: {email}',
                f'Email content: {email}',
                message_template.format(custom_message=prompt),
                'Generate a response for this sender',
                "You are a helpful AI bot that drafts out email responses based on the sender's tone and adds the receiver's name."
            ]
            response = self.model.generate_content("\n".join(messages))
            return response.text.strip()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Email response generation error: {str(e)}")