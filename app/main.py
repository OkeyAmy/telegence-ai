"""
FastAPI application setup and route definitions for the AI Message Response System.
"""

# @Codebase

from fastapi import FastAPI, HTTPException
from app.models.model import EmailRequest, MessageRequest, Response
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
    return {"message": "Welcome to the AI Message Response System"}

@app.post("/greet_user", response_model=Response)
async def greeting():
    """Generate an AI greeting message."""
    try:
        greeting_message = await ai_service.greet_user("Hello")
        return Response(response=greeting_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/write_message", response_model=Response)
async def select_message(request: MessageRequest):
    """Generate an AI response for a user message."""
    try:
        response = await ai_service.generate_response(request.type, request.user_message)
        return Response(email=request.email, response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/respond_message", response_model=Response)
async def respond_to_email(request: EmailRequest):
    """Generate an AI response for an email."""
    try:
        response_message = await ai_service.email_responder(
            request.email_address, request.email, request.prompt, request.type
        )
        return Response(email=request.email_address, response=response_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
