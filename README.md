# Telegence AI Message Response System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A modern AI-powered message response system built with FastAPI and Google's Generative AI. Generate contextual responses for messages and emails across various platforms including WhatsApp, LinkedIn, Slack, and Gmail.

## 🚀 Features

- 🤖 **AI-powered response generation** using Google's Generative AI (gemini-1.5-flash model)
- 📝 **Support for formal, casual, and custom message styles**
- 📧 **Smart email response generation**
- ✉️ **Message writing capabilities**: Automatically generate messages based on user input, tailored to various contexts and platforms.
- 🔄 **Platform integration** (WhatsApp, LinkedIn, Slack, Gmail)
- 🔄 **Message response generation**: Respond to incoming messages with contextually relevant replies.
- 🛡️ **Robust error handling and input validation**
- 🔍 **Interactive API documentation** available via Swagger UI and ReDoc

## 📋 Prerequisites

- Python 3.12 or higher
- Docker and Docker Compose (optional)
- Google API Key for Gemini AI

## ⚡️ Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/telegence-ai.git
   cd telegence-ai
   ```

2. **Set up environment**
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Windows
   .\venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   # Create .env file
   cp .env.example .env
   # Add your Google API key to .env
   GOOGLE_API_KEY=your_google_api_key
   ```

4. **Start the application**
   ```bash
   # Using uvicorn
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

   # Using Docker
   docker-compose up --build
   ```

## 🐳 Docker Support

Run the application using Docker:
```bash
# Build and start containers
docker-compose up --build

# Stop containers
docker-compose down
```

## 🔌 API Endpoints

### Base URL
```
http://localhost:8000
```

### Available Endpoints

| Method | Endpoint          | Description                               |
|--------|-------------------|-------------------------------------------|
| GET    | `/`                | Welcome message                          |
| POST   | `/greet_user`     | Generate AI greeting                     |
| POST   | `/write_message`   | Generate AI response for user messages   |
| POST   | `/respond_message` | Generate AI response for incoming messages |

### Example Request for Writing a Message

```json
POST /write_message
{
    "type": "casual",
    "user_message": "Can you help me with my project update?",
    "email": "user@example.com"
}
```

### Example Response for Writing a Message

```json
{
  "email": "user@example.com",
  "response": "Subject: Need a Hand with My Project Update! 🤘\n\nHey there! 👋\n\nCould you lend a helping hand with my project update? I'm feeling a little stuck and could really use some of your awesome AI brainpower. 😊\n\nThanks a bunch!"
}
```

### Example Request for Responding to a Message

```json
POST /respond_message
{
  "email_address": "user@example.com",
  "email": "What are the next steps for the project Peter?",
  "prompt": "We will start with onboarding",
  "type": "formal"
}
```

### Example Response for Responding to a Message

```json
{
  "email": "user@example.com",
  "response": "Hi [Sender Name],\n\nThe next steps for the project will be to start with onboarding. \n\nBest, \nPeter"
}
```

## 📚 Documentation

Access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔒 Error Handling

The API returns structured error responses:

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "type"
      ],
      "msg": "Field required",
      "input": {
        "email_address": "user@example.com",
        "email": "What are the next steps for the project?",
        "prompt": "We will start with onboarding"
      }
    }
  ]
}
```


## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Google Generative AI](https://ai.google.dev/)
- [Docker](https://www.docker.com/)

---
Made with ❤️ by Telegence Team
