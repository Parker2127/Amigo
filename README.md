# 🫂 AMIGO - AI Therapy Chatbot

**Your compassionate AI therapy companion providing empathetic, context-aware therapeutic responses**

AMIGO is a Flask-based AI therapy chatbot that offers two primary modes of operation:
1. **Google Dialogflow Webhook Integration** - For enterprise conversational AI platforms
2. **Live Chat Interface** - A standalone web application for direct user interaction

## ✨ Features

### 🧠 Core Therapeutic Capabilities
- **Empathetic Response Generation** - Provides validation-focused, therapeutic responses
- **Intent-Based Routing** - Intelligent mapping of user messages to specialized therapeutic handlers
- **Context Management** - Maintains conversation context for multi-turn therapeutic sessions
- **Emotional Validation** - Dedicated responses for sadness, anxiety, anger, and positive emotions
- **Coping Strategy Delivery** - Includes breathing exercises, grounding techniques, and positive affirmations
- **Crisis Resource Integration** - Provides immediate access to crisis helplines and emergency resources

### 💻 Technical Features
- **Dual Interface Support** - Both webhook API and standalone web interface
- **Modular Architecture** - Clean separation between server logic, intent handling, and response content
- **Response Variation System** - Multiple response variants prevent repetitive interactions
- **Loading Screens** - Professional user experience with animated loading states
- **Responsive Design** - Bootstrap-based dark theme optimized for therapy conversations
- **Session Management** - Secure session handling for conversation continuity

### 🎨 User Interface
- **Professional Dark Theme** - Easy on the eyes with Bootstrap styling
- **Message Bubbles** - Distinct styling for user and AMIGO messages with avatars
- **Quick Action Buttons** - One-click access to common therapeutic requests
- **Typing Indicators** - Visual feedback during response generation
- **Crisis Advisory** - Prominent display of emergency helpline information
- **Single-Page Layout** - Full conversation fits on screen without scrolling

## 📋 Prerequisites

- Python 3.8+
- Flask web framework
- Modern web browser for the live chat interface
- Google Dialogflow account (optional, for webhook integration)

- ## 🚀 Live Demo
Want to talk to Amigo ? : [**Live Demo**](https://churn-metrics.replit.app)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/amigo-therapy-chatbot.git
cd amigo-therapy-chatbot
```

### 2. Install Dependencies
```bash
pip install flask gunicorn
```

### 3. Set Environment Variables
```bash
# Required for session security
export SESSION_SECRET="your-secure-secret-key"

# Optional: For database integration
export DATABASE_URL="your-database-url"
```

### 4. Run the Application
```bash
# Development mode
python main.py

# Production mode with Gunicorn
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

### 5. Access the Application
- **Live Chat Interface**: http://localhost:5000
- **Webhook Endpoint**: http://localhost:5000/webhook (for Dialogflow)
- **Developer Information**: http://localhost:5000/webhook-info

## 📁 Project Structure

```
amigo-therapy-chatbot/
├── app.py                 # Main Flask application with routes and web interface
├── intent_handlers.py     # Intent routing and handler functions
├── responses.py          # Therapeutic response content and coping strategies
├── main.py              # Application entry point
├── replit.md            # Project documentation and architecture notes
└── README.md            # This documentation
```

### Core Components

#### `app.py` - Main Application
- Flask server setup and configuration
- Webhook endpoint for Dialogflow integration
- Live chat web interface with HTML/CSS/JavaScript
- Session management and security
- Error handling and logging

#### `intent_handlers.py` - Intent Processing
- Central intent dispatcher mapping user inputs to handlers
- Specialized handler functions for different emotional states
- Context management for multi-turn conversations
- Response selection and formatting

#### `responses.py` - Content Repository
- Therapeutic response variations organized by intent type
- Emotional validation responses for different feelings
- Structured coping strategies (breathing, grounding, affirmations)
- Crisis intervention and resource information

## 🔌 API Documentation

### Webhook Endpoint

**POST /webhook**

Accepts Dialogflow webhook requests and returns structured responses.

#### Request Format
```json
{
  "queryResult": {
    "intent": {
      "displayName": "express_anxiety"
    },
    "queryText": "I'm feeling anxious",
    "parameters": {},
    "outputContexts": []
  },
  "session": "projects/your-project/agent/sessions/session-id"
}
```

#### Response Format
```json
{
  "fulfillmentText": "I understand that you're feeling anxious...",
  "outputContexts": [
    {
      "name": "projects/your-project/agent/sessions/session-id/contexts/anxiety-support",
      "lifespanCount": 5,
      "parameters": {
        "emotion": "anxiety",
        "support_provided": true
      }
    }
  ]
}
```

### Chat API Endpoint

**POST /chat**

Processes direct chat messages from the web interface.

#### Request Format
```json
{
  "message": "I need help with breathing exercises"
}
```

#### Response Format
```json
{
  "response": "Great idea! I love box breathing - it's so simple but really effective..."
}
```

## 🎯 Supported Intents

### Emotional Expression
- **express_sadness** - Validates and responds to sadness with empathy
- **express_anxiety** - Provides anxiety support and coping strategies
- **express_anger** - Helps process anger with validation and techniques
- **positive_wellbeing** - Celebrates and reinforces positive emotions

### Therapeutic Requests
- **ask_coping_strategy** - Delivers various coping strategies based on context
- **breathing_exercise** - Guides through specific breathing techniques
- **grounding_technique** - Provides sensory grounding exercises
- **positive_affirmation** - Offers personalized affirmations

### Conversation Management
- **greeting** - Warm, welcoming responses to start conversations
- **check_in** - Regular check-ins during ongoing conversations
- **goodbye** - Supportive closure with continued support reminders
- **fallback** - Gentle redirection for unrecognized inputs

## 🏗️ Architecture

### Request Processing Flow
1. **Input Reception** - Dialogflow or web interface sends user message
2. **Intent Detection** - System identifies emotional state and therapeutic need
3. **Handler Routing** - Intent dispatcher routes to specialized handler function
4. **Response Generation** - Handler selects appropriate therapeutic response
5. **Context Management** - Session context updated for conversation continuity
6. **Response Delivery** - Formatted response returned to user interface

### Design Principles
- **Modular Design** - Clear separation of concerns between components
- **Extensible Architecture** - Easy to add new intents and response types
- **Validation-First Approach** - All responses prioritize emotional validation
- **Context Awareness** - Maintains conversation state for personalized support
- **Safety Integration** - Crisis resources prominently available throughout

## 🔧 Development

### Adding New Intents

1. **Define Intent Handler** in `intent_handlers.py`:
```python
def handle_new_intent(parameters, query_text, session_id, input_contexts):
    responses = get_response_variants('new_intent')
    return {
        'text': random.choice(responses),
        'output_contexts': []
    }
```

2. **Add Response Variants** in `responses.py`:
```python
'new_intent': [
    "First response option...",
    "Second response option...",
    "Third response option..."
]
```

3. **Register Intent** in the `intent_handlers` dictionary:
```python
intent_handlers = {
    # existing intents...
    'new_intent': handle_new_intent,
}
```

### Response Guidelines
- Lead with validation and empathy
- Offer concrete, actionable support
- Maintain hope and encouragement
- Include crisis resources when appropriate
- Use warm, conversational language

### Testing
- Test both webhook and live chat interfaces
- Verify all intent handlers work correctly
- Check response variation randomization
- Test session management and context handling
- Validate crisis resource accessibility

## 🚦 Deployment

### Environment Variables
```bash
# Required
SESSION_SECRET=your-secure-secret-key

# Optional
DATABASE_URL=your-database-connection-string
PORT=5000
```

### Production Deployment
The application is configured to run with Gunicorn for production:

```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

### Platform Deployment
- **Replit**: Ready to deploy with included configuration
- **Heroku**: Add `Procfile` with gunicorn command
- **Docker**: Create Dockerfile with Python and Flask setup
- **Cloud Functions**: Adapt webhook endpoint for serverless deployment

## 🛡️ Safety and Ethical Considerations

### Crisis Resources
- **988 Suicide & Crisis Lifeline** prominently displayed
- **Emergency services (911)** clearly accessible
- Crisis resources integrated throughout interface

### Important Disclaimers
- AMIGO is **not a replacement** for professional mental health treatment
- Users in crisis should contact emergency services or crisis hotlines immediately
- All conversations are for supportive purposes only
- The application maintains user privacy and does not store personal information

### Responsible AI Practices
- Responses focus on validation and support rather than diagnosis
- System avoids providing medical or clinical advice
- Crisis situations are redirected to professional resources
- User safety is prioritized in all response design

## 🤝 Contributing

We welcome contributions that enhance AMIGO's therapeutic capabilities:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/new-coping-strategy`)
3. **Make your changes** following the response guidelines
4. **Test thoroughly** with both interfaces
5. **Submit a pull request** with clear description

### Contribution Guidelines
- All new responses should prioritize empathy and validation
- Include multiple response variations to avoid repetition
- Test changes with the live chat interface
- Maintain the existing code structure and patterns
- Document any new intents or features

## 📄 License

This project is open source. Please ensure any deployment complies with relevant healthcare and privacy regulations in your jurisdiction.

## 🆘 Support

For technical issues or therapeutic content improvements, please open an issue on GitHub.

**Remember: If you're in crisis, please contact emergency services (911) or the 988 Suicide & Crisis Lifeline immediately.**

---

*AMIGO - Because everyone deserves compassionate support* 💙
