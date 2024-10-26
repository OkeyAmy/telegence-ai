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


class MessageRequest(BaseModel):
    type: str
    user_message: str
    email: Optional[str] = None 


#  Define Response model with methods for handling null values
class Response(BaseModel):
    email: Optional[str] = None
    response: str

    # class Config:
    #     json_encoders = {
    #         Optional[str]: lambda v: v or None
    #     }

    # def dict(self, *args, **kwargs):
    #     return {k: v for k, v in super().dict(*args, **kwargs).items() if v is not None}

    # @classmethod
    # def from_dict(cls, data: dict):
    #     return cls(**{k: v for k, v in data.items() if v is not None})

    # def json(self, *args, **kwargs):
    #     return super().json(*args, **kwargs, exclude_none=True)
