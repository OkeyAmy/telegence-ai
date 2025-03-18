# Telegence AI Message Response System

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🌟 Project Overview

Telegence is an advanced AI-powered message response system that leverages Google's Generative AI to create intelligent, context-aware email and message responses. The project aims to streamline communication by providing smart, personalized AI-generated responses across various platforms and communication styles.

## 🚀 Key Features

- 🤖 Advanced AI-Powered Response Generation
- 📧 Intelligent Email and Message Formatting
- 🎨 Highly Personalized Responses
- 🔒 Secure AI Key Management
- 📝 Flexible Message Tones and Styles
- 🌐 Multi-Platform Compatibility

## 🛠 Technologies Used

- **Backend Framework**: FastAPI
- **AI Model**: Google Generative AI (Gemini 2.0 Flash)
- **Programming Language**: Python 3.11+
- **Deployment**: Render
- **Frontend Integration**: Compatible with various web applications




### Software Prerequisites
- Python 3.11+
- pip 21.0+ or poetry
- Git
- Google AI API Key

## 🔧 Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/OkeyAmy/telegence-ai.git
cd telegence-ai
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Using pip
pip install -r requirements.txt

# Or using poetry
poetry install
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```
# Google AI API Configuration
GOOGLE_API_KEY=your_google_generative_ai_key_here

# Optional Configurations
LOG_LEVEL=INFO
```

## 🌈 API Endpoints and Request Structures

### 1. `/write_message` Endpoint
**Purpose**: Generate email responses based on user input

**Required Fields**:
```json
{
    "type": "string",            // Required: Message tone (e.g., "formal", "casual", or any custom tone)
    "user_message": "string",    // Required: The content of the message to be responded to
    "email": "string",   // Optional: Sender's email address
    "user_name": "string"        // Optional: Sender's name for personalization
}
```

**Response Model**:
```json
{
    "email": "string",   // Generated or provided email address
    "subject": "string",         // AI-generated email subject
    "body": "string",            // AI-generated email body
    "user_name": "string"        // Sender's name (if provided)
}
```

### 2. `/respond_message` Endpoint
**Purpose**: Generate contextual email responses to existing emails

**Required Fields**:
```json
{
    "email_address": "string",   // Required: Recipient's email address
    "email": "string",           // Required: Original email content
    "prompt": "string",          // Required: User's response or action
    "type": "string",            // Required: Message tone (e.g., "formal", "casual", or custom tone)
    "user_name": "string"        // Optional: Sender's name
}
```

**Response Model**:
```json
{
    "email_address": "string",   // Recipient's email address
    "response": "string",        // AI-generated email response
    "user_name": "string"        // Sender's name (if provided)
}
```

### 3. `/greet_user` Endpoint
**Purpose**: Generate personalized greetings

**Required Fields**:
```json
{
    "user_name": "string"        // Optional: User's name for personalization
}
```

**Response Model**:
```json
{
    "response": "string",        // AI-generated greeting
    "user_name": "string"        // User's name (if provided)
}
```

## 📊 Supported Message Types and Tones

- `formal`: Professional, corporate communication
- `casual`: Friendly, conversational tone
- `technical`: Detailed, precise language
- `empathetic`: Supportive, understanding communication
- Custom Tones: Fully customizable based on user input

## 🔐 Security Features

- Server-side AI key management
- Optional API key authentication
- Safety settings to prevent harmful content generation
- Secure environment variable handling
- Input validation and sanitization

## 🐳 Docker Support

### Building Docker Image
```bash
docker build -t telegence-ai .
```

### Running Docker Container
```bash
docker run -p 8000:8000 telegence-ai
```

## 📚 API Documentation

Access interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`



## 📝 Logging

- Comprehensive logging with debug and info levels
- Configurable log levels
- Supports multiple log handlers

## 🚀 Deployment

### Render Deployment
1. Connect GitHub repository
2. Set environment variables
3. Choose Python buildpack
4. Deploy main branch

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📋 Roadmap

- [ ] Add more AI models feature for personalization
- [ ] Implement advanced caching
- [ ] Create frontend dashboard
- [ ] Enhance multi-language support

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Contact

Okey Amy
- GitHub: [@OkeyAmy](https://github.com/OkeyAmy)
- Project Link: [https://github.com/OkeyAmy/telegence-ai](https://github.com/OkeyAmy/telegence-ai)
- X: [X](https://x.com/okey_amy)

---
Made with ❤️ by Okey Amy for the love of AI and trying out cool APIs. Check out my other API repositories!
