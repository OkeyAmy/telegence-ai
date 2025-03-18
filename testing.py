"""
Message templates and types for generating AI responses in the Message Response System.
"""

from enum import Enum
from langchain.prompts import PromptTemplate
import json
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ... Define MessageType enum for different message styles
class MessageType(str, Enum):
    FORMAL = "formal"
    CASUAL = "casual"
    CUSTOM = "custom"

# ... Define message templates for each message type
MESSAGE_TEMPLATES = {
    MessageType.FORMAL: PromptTemplate(
        input_variables=["custom_message"],
        template="You are a helpful AI assistant. Generate a formal response based on this message: {custom_message}"
    ),
    MessageType.CASUAL: PromptTemplate(
        input_variables=["custom_message"],
        template="You are a helpful AI assistant that communicates casually. Generate a response based on this message: {custom_message}"
    ),
    MessageType.CUSTOM: PromptTemplate(
        input_variables=["custom_message"],
        template="{custom_message}"
    )
}

from typing import List, Optional
import google.generativeai as genai
from fastapi import HTTPException
from app.config import get_settings
from app.templates.templates import MessageType, MESSAGE_TEMPLATES

# services.py
class AIService:
    """
    A service for generating AI-powered email responses with different message styles.

    Attributes:
        model (genai.GenerativeModel): The Gemini AI model used for generating responses.

    Methods:
        generate_response(message_type: str, user_message: str) -> dict:
            Generates an email response based on the given message type and user message.
    """

    def __init__(self):
        """
        Initialize the AIService by configuring the Google Generative AI model.
        """
        settings = get_settings()
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    async def generate_response(self, message_type: str, user_message: str) -> dict:
        """
        Generate an email response for a given message.

        Args:
            message_type (str): The type of message style to use. 
                Must be one of 'formal', 'casual', or 'custom'.
            user_message (str): The original message to be transformed into an email.

        Returns:
            dict: A dictionary containing 'email', 'subject', and 'body' keys.

        Raises:
            HTTPException: For various error conditions during email generation.

        Examples:
            >>> ai_service = AIService()
            >>> response = await ai_service.generate_response('formal', 'Need help with project')
            >>> print(response)
            {
                'email': 'support@example.com',
                'subject': 'Project Assistance Request',
                'body': 'Dear Support Team, ...'
            }
        """
        try:
            logger.info(f"Generating response for message type: {message_type}")
            template = self._get_message_template(message_type)
            prompt = template.format(custom_message=user_message)

            email_generation_prompt = f"""
            Rewrite the given message into an email format. The email should include a subject and body.
            Please always sign the email for the user. 
            The output MUST be a valid JSON object with the following keys: 
            - "email": A valid email address
            - "subject": A concise email subject
            - "body": A detailed email body

            Original message: {prompt}

            IMPORTANT: Respond ONLY with a valid JSON object. No additional text.
            Example:
            {{
                "email": "support@example.com",
                "subject": "Assistance Request",
                "body": "Dear Support Team, I am writing to request help..."
            }}
            """
            
            logger.debug(f"Email generation prompt: {email_generation_prompt}")

            # Generate content with safety settings to prevent problematic responses
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
            
            response = self.model.generate_content(
                email_generation_prompt, 
                safety_settings=safety_settings
            )
            
            logger.debug(f"Raw AI response: {response.text}")
            
            json_str = response.text.strip().replace('```json', '').replace('```', '').strip()
            
            # Parse the JSON response
            try:
                email_data = json.loads(json_str)
                logger.info("Successfully parsed email response")
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {e}")
                logger.error(f"Problematic JSON string: {json_str}")
                raise HTTPException(status_code=400, detail=f"Invalid JSON response: {str(e)}")

            # Ensure keys are lowercase
            normalized_data = {k.lower(): v for k, v in email_data.items()}

            # Validate required fields
            required_fields = ["email", "subject", "body"]
            for field in required_fields:
                if field not in normalized_data:
                    raise ValueError(f"Missing required field: {field}")

            return {
                "email": normalized_data["email"],
                "subject": normalized_data["subject"],
                "body": normalized_data["body"]
            }

        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode Error: {e}")
            raise HTTPException(status_code=400, detail=f"Invalid JSON response: {str(e)}")
        except ValueError as e:
            logger.error(f"Validation Error: {e}")
            raise HTTPException(status_code=422, detail=str(e))
        except Exception as e:
            logger.error(f"Error in generate_response: {str(e)}")
            raise HTTPException(status_code=500, detail=f"AI generation error: {str(e)}")

    def _get_message_template(self, message_type: str) -> str:
        """
        Retrieve the appropriate message template based on the message type.

        Args:
            message_type (str): The type of message style.

        Returns:
            PromptTemplate: The corresponding message template.

        Examples:
            >>> service = AIService()
            >>> template = service._get_message_template('formal')
            >>> template  # Returns a PromptTemplate for formal messages
        """
        try:
            return MESSAGE_TEMPLATES[MessageType(message_type)]
        except ValueError:
            return MESSAGE_TEMPLATES[MessageType.CUSTOM]

# Example usage function with logging
async def example_usage():
    """
    Demonstrate how to use the AIService for generating email responses.
    """
    logger.info("Starting example usage of AIService")
    
    # Create an instance of AIService
    ai_service = AIService()

    try:
        # Generate a formal email response
        logger.info("Generating formal email response")
        formal_response = await ai_service.generate_response(
            message_type='formal', 
            user_message='I need assistance with my project deadline'
        )
        logger.info(f"Formal email response generated: {formal_response}")
        print("Formal Email Response:", formal_response)

        # Generate a casual email response
        logger.info("Generating casual email response")
        casual_response = await ai_service.generate_response(
            message_type='casual', 
            user_message='Hey, can you help me with something?'
        )
        logger.info(f"Casual email response generated: {casual_response}")
        print("Casual Email Response:", casual_response)

    except Exception as e:
        logger.error(f"Error in example usage: {str(e)}")
        print(f"Error generating email: {e}")

# Optional: Run the example if this script is executed directly
if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())