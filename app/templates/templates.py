"""
Message templates and types for generating AI responses in the Message Response System.
"""

from enum import Enum
from langchain.prompts import PromptTemplate

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