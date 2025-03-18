from typing import List, Optional
import google.generativeai as genai
from fastapi import HTTPException
from app.config import get_settings
from app.templates.templates import MessageType, MESSAGE_TEMPLATES

import logging
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# services.py
class AIService:
    def __init__(self):
        settings = get_settings()
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    async def greet_user(self, message: str, user_name: str = None) -> str:
        try:
            # Personalize the greeting if user_name is provided
            if user_name:
                personalized_message = f"""
                Task: Generate a warm, friendly greeting
                Context:
                - Recipient's name: {user_name}
                - Initial message: {message}

                Instructions:
                1. Create a personalized greeting that addresses {user_name} directly
                2. The tone should be friendly and welcoming
                3. Offer assistance or ask how you can help
                4. Keep the response concise and natural

                Example format:
                "Hi [Name]! It's great to meet you. I'm here to help with [context]. What can I assist you with today?"
                """
            else:
                personalized_message = f"""
                Task: Generate a warm, friendly greeting
                Context:
                - Initial message: {message}

                Instructions:
                1. Create a friendly, generic greeting
                2. Offer assistance or ask how you can help
                3. Keep the response concise and welcoming
                4. Do not mention a specific name

                Example format:
                "Hello there! I'm ready to help. What can I assist you with today?"
                """
            
            greeting = self.model.generate_content(personalized_message)
            logger.debug(f"Generated greeting: {greeting.text}")
            return greeting.text.strip()
        except Exception as e:
            logger.error(f"AI greeting error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"AI greeting error: {str(e)}")

    async def generate_response(
        self, 
        message_type: str, 
        user_message: str, 
        email: Optional[str] = None, 
        user_name: Optional[str] = None
    ) -> dict:
        try:
            template = self._get_message_template(message_type)

            prompt = template.format(custom_message=user_message)
            # Construct the prompt without relying on separate templates
            email_generation_prompt = f"""
            With this prompt: {prompt}
            Task: Convert the Following Message into a Professional Email
            Original Message: "{user_message}"

            Instructions:
            1. Format the message into a complete email structure
            2. Maintain the message's core intent
            3. Use the sender's information:
               - Email: {email}
               - Sender's Name: {user_name} (if provided)
            4. Match the tone to the message type: {message_type}

            Email Requirements:
            - Include a subject line that reflects the message's intent
            - Body must:
               - Start with a greeting (e.g., "Dear Team,")
               - Include the original message as the core content
               - End with a professional sign-off using the sender's name which is {user_name}
            - Output strictly in JSON format with these keys: "email", "subject", "body"
            
            Example Input:
            {{
                "type": "formal",
                "user_message": "Thank you for attending my party last night.",
                "email": "okey@example.com",
                "user_name": "Okey"
            }}

            Example Output:
            {{
                "subject": "Appreciation for Attending My Party",
                "body": "Dear Friend,\n\nThank you for attending my party last night. Your presence made the event even more special, and I truly appreciate you taking the time to join me.\n\nBest regards,\nOkey"
            }}

            Example Input:
            {{
                "type": "casual",
                "user_message": "Thanks for coming to my party last night!",
                "email": "alex@example.com",
                "user_name": "Alex"
            }}

            Example Output:
            {{
                "subject": "Thanks for Coming to My Party",
                "body": "Hey [Friend's Name],\n\nThanks for coming to my party last night! It was so much fun having you there, and I really appreciate it.\n\nCheers,\nAlex"
            }}

            CRITICAL NOTES:
            - Do NOT respond to the message - format it into an email
            - Use the provided email and name exactly as given
            - Ensure valid JSON with all required fields
            - The original message must be the central content of the body
            - Keep the email structure natural and conversational
            """
            
            # Generate content with safety settings
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]

            response = self.model.generate_content(email_generation_prompt, safety_settings=safety_settings)
            logger.debug(f"Raw Response: {response.text}")
            
            # Clean and parse JSON response
            json_str = response.text.strip().replace('```json', '').replace('```', '').strip()
            logger.debug(f"JSON String: {json_str}")

            try:
                email_data = json.loads(json_str)
            except json.JSONDecodeError as e:
                logger.error(f"JSON Decode Error: {e}")
                raise HTTPException(status_code=400, detail=f"Invalid JSON response: {str(e)}")

            # Validate required fields
            required_fields = ["subject", "body"]
            for field in required_fields:
                if field not in email_data:
                    raise ValueError(f"Missing required field: {field}")

            # Ensure proper email handling
            final_email = email or "user@example.com"

            return {
                "email": final_email,
                "subject": email_data["subject"],
                "body": email_data["body"]
            }

        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode Error: {e}")
            raise HTTPException(status_code=400, detail=f"Invalid JSON response: {str(e)}")
        except ValueError as e:
            logger.error(f"Validation Error: {e}")
            raise HTTPException(status_code=422, detail=str(e))
        except Exception as e:
            logger.error(f"Unexpected Error: {e}")
            raise HTTPException(status_code=500, detail=f"AI generation error: {str(e)}")

    async def email_responder(
        self,
        email_address: str,
        email: str,
        prompt: str,
        message_type: str,
        user_name: Optional[str] = None
    ) -> str:
        try:
            # Get the message template based on the message type
            message_template = self._get_message_template(message_type)

            # Construct a detailed, context-aware prompt
            detailed_prompt = f"""Task: Generate a Precise Email Response

Response Generation Criteria:
1. Input Context:
   - Original Email: "{email}"
   - User Prompt: "{prompt}"
   - Desired Tone: {message_type}
   - Sender's Name Reference: {user_name}

2. Structural Requirements:
   - Omit any "Subject:" line
   - Begin with an appropriate, context-specific greeting
   - Directly address the content of the original email
   - Incorporate the user's prompt seamlessly
   - Conclude with a professional sign-off

3. Signature Guidelines:
   - Prioritize detecting a name from the original email
   - If no name is detected, use "{user_name}" as the signature
   - If no user name is available, use a generic "Team" signature

4. Tone Adaptation:
   - Maintain a {message_type.lower()} communication style
   - Ensure professional and clear language
   - Match the emotional tenor of the original email

5. Response Template:
   [Greeting],

   [Response Content Addressing Original Email and Prompt]

   Best regards,
   [Signature Name]

Practical Example:
Original Email: "Hi Okey, I need an update on the project status."
Prompt: "AI integration is complete, preparing for GitHub push"
Response: "Hi Okey,

Thanks for checking in about the project status. The AI integration is now complete, and I'm currently preparing for the GitHub repository push. I'll send a detailed update once everything is live.

Best regards,
{user_name or 'Team'}"""

            # Generate the response using the model
            response = self.model.generate_content(detailed_prompt)

            return response.text.strip()

        except Exception as e:
            logger.error(f"Email response generation error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Email response generation error: {str(e)}")

    def _get_message_template(self, message_type: str) -> str:
        try:
            return MESSAGE_TEMPLATES[MessageType(message_type)]
        except ValueError:
            return MESSAGE_TEMPLATES[MessageType.CUSTOM]
