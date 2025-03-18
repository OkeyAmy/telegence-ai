"""
Data models for request and response objects in the AI Message Response System.
"""

# @Codebase

from pydantic import BaseModel
from typing import Optional


class EmailRequest(BaseModel):
    email_address: str
    email: Optional[str] = None
    prompt: str
    type: str
    user_name: Optional[str] = None  # Added user_name field


class MessageRequest(BaseModel):
    type: str
    user_message: str
    email: Optional[str] = None 
    user_name: Optional[str] = None  # Added user_name field


#  Define Response model with methods for handling null values
class Response(BaseModel):
    email: Optional[str] = None
    response: str
    user_name: Optional[str] = None  # Added user_name field


class EmailWriter(BaseModel):
    """
    Model for representing an email with its key components.
    
    Attributes:
        email (str): The recipient's email address
        subject (str): The email subject line
        body (str): The email body content
        user_name (Optional[str]): The name of the user
    """
    email: str
    subject: str
    body: str
    user_name: Optional[str] = None  # Added user_name field
