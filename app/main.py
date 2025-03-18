"""
FastAPI application setup and route definitions for the AI Message Response System.
"""

# @Codebase

import logging
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from fastapi import FastAPI, HTTPException
from app.models.model import EmailRequest, MessageRequest, Response, EmailWriter
from app.services.services import AIService

app = FastAPI(
    title="Telegence AI Message Response System",
    description="API for generating AI-based responses for user messages and emails.",
    version="0.1.0"
)

ai_service = AIService()

@app.get("/")
async def read_root():
    """Return a welcome message."""
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the AI Message Response System"}

@app.post("/greet_user", response_model=Response)
async def greeting(user_name: str = None):
    """Generate an AI greeting message."""
    try:
        logger.info(f"Generating user greeting for user: {user_name}")
        greeting_message = await ai_service.greet_user("Hello", user_name)
        logger.info("User greeting generated successfully")
        return Response(response=greeting_message, user_name=user_name)
    except Exception as e:
        logger.error(f"Error generating greeting: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/write_message", response_model=EmailWriter)
async def select_message(request: MessageRequest):
    """Generate an AI response for a user message."""
    try:
        logger.info(f"Received write_message request: type={request.type}, message={request.user_message}, user_name={request.user_name}")
        response = await ai_service.generate_response(
            request.type, 
            request.user_message, 
            request.email,
            request.user_name
        )
        
        email_response = EmailWriter(
            email=request.email or "user@example.com", 
            subject=response["subject"], 
            body=response["body"],
            user_name=request.user_name
        )
        
        logger.info(f"Generated email response with subject: {email_response.subject}")
        return email_response
    except Exception as e:
        logger.error(f"Error in write_message endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/respond_message", response_model=Response)
async def respond_to_email(request: EmailRequest):
    """Generate an AI response for an email."""
    try:
        logger.info(f"Received respond_message request for email: {request.email_address}, user_name: {request.user_name}")
        response_message = await ai_service.email_responder(
            request.email_address, 
            request.email, 
            request.prompt, 
            request.type,
            request.user_name
        )
        logger.info("Email response generated successfully")
        return Response(
            email=request.email_address, 
            response=response_message, 
            user_name=request.user_name
        )
    except Exception as e:
        logger.error(f"Error in respond_message endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting AI Message Response System")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
