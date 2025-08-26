import os
import logging
from flask import Flask, request, jsonify, render_template_string, session
from intent_handlers import handle_intent
import uuid

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "amigo-therapy-bot-secret")

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Main webhook endpoint to receive requests from Google Dialogflow
    """
    try:
        # Parse the incoming JSON request from Dialogflow
        req = request.get_json()
        
        if not req:
            logging.error("No JSON payload received")
            return jsonify({
                "fulfillmentText": "I'm sorry, I didn't receive your message properly. Could you please try again?"
            }), 400
        
        # Extract intent information
        intent_info = req.get('queryResult', {}).get('intent', {})
        intent_name = intent_info.get('displayName', '')
        
        # Extract parameters and query text
        parameters = req.get('queryResult', {}).get('parameters', {})
        query_text = req.get('queryResult', {}).get('queryText', '')
        session_id = req.get('session', '').split('/')[-1] if req.get('session') else 'unknown'
        
        # Extract input contexts for conversation state
        input_contexts = req.get('queryResult', {}).get('outputContexts', [])
        
        logging.info(f"Received intent: {intent_name} from session: {session_id}")
        logging.debug(f"Query text: {query_text}")
        logging.debug(f"Parameters: {parameters}")
        
        # Handle the intent and get response
        response_data = handle_intent(
            intent_name=intent_name,
            parameters=parameters,
            query_text=query_text,
            session_id=session_id,
            input_contexts=input_contexts
        )
        
        # Format response for Dialogflow
        dialogflow_response = {
            "fulfillmentText": response_data.get('text', ''),
            "outputContexts": response_data.get('output_contexts', [])
        }
        
        # Add follow-up event if specified
        if response_data.get('followup_event'):
            dialogflow_response["followupEventInput"] = {
                "name": response_data['followup_event'],
                "parameters": response_data.get('followup_parameters', {})
            }
        
        logging.debug(f"Sending response: {dialogflow_response}")
        return jsonify(dialogflow_response)
    
    except Exception as e:
        logging.error(f"Error processing webhook request: {str(e)}")
        return jsonify({
            "fulfillmentText": "I'm experiencing some technical difficulties right now. Please bear with me, and let's try again in a moment."
        }), 500

@app.route('/chat', methods=['POST'])
def chat():
    """
    Chat endpoint for direct web interface communication
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'response': "I didn't receive your message. Could you please try again?"}), 400
        
        # Get or create session ID
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        
        session_id = session['session_id']
        
        # Detect intent from user message
        detected_intent = detect_intent_from_message(user_message)
        
        logging.info(f"Chat message: {user_message}")
        logging.info(f"Detected intent: {detected_intent}")
        
        # Handle the intent using existing system
        response_data = handle_intent(
            intent_name=detected_intent,
            parameters={},
            query_text=user_message,
            session_id=session_id,
            input_contexts=[]
        )
        
        return jsonify({
            'response': response_data.get('text', ''),
            'intent': detected_intent
        })
        
    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'response': "I'm experiencing some technical difficulties right now. Please bear with me, and let's try again in a moment."
        }), 500

def detect_intent_from_message(message):
    """
    Simple intent detection based on keywords and patterns
    """
    message_lower = message.lower()
    
    # Check more specific patterns first to avoid false matches
    
    # Positive emotions and wellbeing (check early to celebrate good moments)
    if any(phrase in message_lower for phrase in ['i am good', 'i\'m good', 'feeling good', 'doing well', 'i\'m great', 'i am great', 'feeling better', 'much better', 'doing better', 'i\'m fine', 'i am fine', 'feeling fine', 'i\'m okay', 'i am okay', 'feeling happy', 'feeling positive']):
        return 'positive_wellbeing'
    
    # Breathing exercise patterns (check first - most specific)
    if any(phrase in message_lower for phrase in ['breathing exercise', 'breathing technique', 'need a breathing', 'breathing help']):
        return 'breathing_exercise'
    
    # Grounding technique patterns
    if any(phrase in message_lower for phrase in ['grounding', 'ground me', 'present moment', 'grounding technique']):
        return 'grounding_technique'
    
    # Coping strategy patterns
    if any(phrase in message_lower for phrase in ['coping strategy', 'coping mechanism', 'help me cope', 'need coping help', 'what can i do', 'how do i']):
        return 'ask_coping_strategy'
    
    # Positive affirmation patterns
    if any(phrase in message_lower for phrase in ['affirmation', 'positive thoughts', 'encourage me', 'motivation', 'need encouragement']):
        return 'positive_affirmation'
    
    # Sadness patterns
    if any(word in message_lower for word in ['sad', 'depressed', 'down', 'upset', 'cry', 'crying', 'heartbroken', 'grief', 'feel sad']):
        return 'express_sadness'
    
    # Anxiety patterns
    if any(word in message_lower for word in ['anxious', 'anxiety', 'worried', 'nervous', 'panic', 'stress', 'overwhelmed', 'feel anxious']):
        return 'express_anxiety'
    
    # Anger patterns
    if any(word in message_lower for word in ['angry', 'mad', 'furious', 'frustrated', 'annoyed', 'irritated', 'feel angry']):
        return 'express_anger'
    
    # Check-in patterns
    if any(phrase in message_lower for phrase in ['how are you', 'checking in', 'check in']):
        return 'check_in'
    
    # Greeting patterns (more specific now)
    if any(word in message_lower for word in ['hello', 'hi there', 'hey', 'good morning', 'good afternoon', 'good evening']) and not any(word in message_lower for word in ['need', 'help', 'feel', 'want']):
        return 'greeting'
    
    # Handle "hi" separately to avoid conflicts
    if message_lower.strip() in ['hi', 'hello', 'hey']:
        return 'greeting'
    
    # Goodbye patterns
    if any(word in message_lower for word in ['bye', 'goodbye', 'see you', 'talk later', 'take care']):
        return 'goodbye'
    
    # Breathing related (less specific patterns)
    if 'breathe' in message_lower or 'calm down' in message_lower:
        return 'breathing_exercise'
    
    # Default fallback for unrecognized patterns
    return 'fallback'

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify the webhook is running
    """
    return jsonify({
        "status": "healthy",
        "service": "AMIGO Therapy Chatbot Webhook",
        "version": "1.0.0"
    })

@app.route('/', methods=['GET'])
def home():
    """
    Main page with chat interface
    """
    return """
    <!DOCTYPE html>
    <html lang="en" data-bs-theme="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AMIGO - AI Therapy Chatbot</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
        <style>
            body {
                height: 100vh;
                overflow: hidden;
            }
            .loading-screen {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: var(--bs-body-bg);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                z-index: 9999;
                transition: opacity 0.5s ease-out;
            }
            .loading-screen.hidden {
                opacity: 0;
                pointer-events: none;
            }
            .loading-spinner {
                width: 50px;
                height: 50px;
                border: 4px solid var(--bs-border-color);
                border-top: 4px solid var(--bs-primary);
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin-bottom: 1rem;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .loading-dots {
                display: inline-flex;
                align-items: center;
                gap: 4px;
            }
            .loading-dots .dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background-color: var(--bs-primary);
                animation: loading-dots 1.4s infinite ease-in-out both;
            }
            .loading-dots .dot:nth-child(1) { animation-delay: -0.32s; }
            .loading-dots .dot:nth-child(2) { animation-delay: -0.16s; }
            @keyframes loading-dots {
                0%, 80%, 100% {
                    transform: scale(0);
                    opacity: 0.5;
                }
                40% {
                    transform: scale(1);
                    opacity: 1;
                }
            }
            .container {
                height: 100vh;
                display: flex;
                flex-direction: column;
                padding: 1rem;
            }
            .header-section {
                flex-shrink: 0;
                margin-bottom: 1rem;
            }
            .chat-card {
                flex: 1;
                display: flex;
                flex-direction: column;
                min-height: 0;
            }
            .chat-container {
                flex: 1;
                overflow-y: auto;
                border: 1px solid var(--bs-border-color);
                border-radius: 0.375rem;
                padding: 1rem;
                background: var(--bs-body-bg);
                min-height: 0;
            }
            .input-section {
                flex-shrink: 0;
                border-top: 1px solid var(--bs-border-color);
                padding: 1rem;
            }
            .footer-section {
                flex-shrink: 0;
                text-align: center;
                margin-top: 0.5rem;
            }
            .message {
                margin-bottom: 1rem;
                display: flex;
                align-items: flex-start;
            }
            .message.user {
                justify-content: flex-end;
            }
            .message.bot {
                justify-content: flex-start;
            }
            .message-content {
                max-width: 70%;
                padding: 0.75rem 1rem;
                border-radius: 1rem;
                position: relative;
            }
            .message.user .message-content {
                background: var(--bs-primary);
                color: white;
                border-bottom-right-radius: 0.25rem;
            }
            .message.bot .message-content {
                background: var(--bs-secondary-bg);
                border: 1px solid var(--bs-border-color);
                border-bottom-left-radius: 0.25rem;
            }
            .message-avatar {
                width: 36px;
                height: 36px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 0.5rem;
                font-size: 1.2rem;
            }
            .message.user .message-avatar {
                background: var(--bs-info);
                order: 2;
            }
            .message.bot .message-avatar {
                background: var(--bs-success);
                order: 1;
            }
            .typing-indicator {
                display: none;
                padding: 1rem;
                color: var(--bs-secondary);
                font-style: italic;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .typing-indicator.show {
                display: flex;
            }
            .quick-actions {
                margin-bottom: 1rem;
            }
            .quick-action-btn {
                margin: 0.25rem;
                font-size: 0.875rem;
            }
        </style>
    </head>
    <body>
        <!-- Loading Screen -->
        <div id="loadingScreen" class="loading-screen">
            <div class="loading-spinner"></div>
            <h2 class="text-primary mb-3">
                <i class="bi bi-heart-pulse"></i> AMIGO
            </h2>
            <p class="text-muted">Preparing your safe space...</p>
            <div class="loading-dots mt-3">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>

        <div class="container">
            <div class="row justify-content-center h-100">
                <div class="col-lg-8 d-flex flex-column h-100">
                    <div class="header-section text-center">
                        <h1 class="h3 fw-bold text-primary mb-1">
                            <i class="bi bi-heart-pulse"></i> AMIGO
                        </h1>
                        <p class="text-muted small mb-0">Your compassionate AI therapy companion</p>
                    </div>
                    
                    <div class="card chat-card">
                        <div class="card-body p-0 d-flex flex-column h-100">
                            <div id="chatContainer" class="chat-container">
                                <div class="message bot">
                                    <div class="message-avatar">
                                        <i class="bi bi-robot"></i>
                                    </div>
                                    <div class="message-content">
                                        <strong>AMIGO</strong><br>
                                        Hello! I'm AMIGO, and I'm here to listen and support you. How are you feeling today?
                                    </div>
                                </div>
                            </div>
                            
                            <div id="typingIndicator" class="typing-indicator">
                                <div class="loading-dots">
                                    <div class="dot"></div>
                                    <div class="dot"></div>
                                    <div class="dot"></div>
                                </div>
                                <span>AMIGO is thinking...</span>
                            </div>
                            
                            <div class="input-section">
                                <div class="quick-actions">
                                    <div class="text-muted small mb-2">Quick options:</div>
                                    <button class="btn btn-outline-secondary btn-sm quick-action-btn" onclick="sendQuickMessage('I feel sad today')">
                                        <i class="bi bi-emoji-frown"></i> Feeling sad
                                    </button>
                                    <button class="btn btn-outline-secondary btn-sm quick-action-btn" onclick="sendQuickMessage('I feel anxious')">
                                        <i class="bi bi-emoji-dizzy"></i> Feeling anxious
                                    </button>
                                    <button class="btn btn-outline-secondary btn-sm quick-action-btn" onclick="sendQuickMessage('Can you help me with a coping strategy?')">
                                        <i class="bi bi-lightbulb"></i> Need coping help
                                    </button>
                                    <button class="btn btn-outline-secondary btn-sm quick-action-btn" onclick="sendQuickMessage('I need a breathing exercise')">
                                        <i class="bi bi-wind"></i> Breathing exercise
                                    </button>
                                </div>
                                
                                <div class="input-group">
                                    <input type="text" id="messageInput" class="form-control" 
                                           placeholder="Share what's on your mind..." 
                                           onkeypress="handleKeyPress(event)">
                                    <button class="btn btn-primary" onclick="sendMessage()">
                                        <i class="bi bi-send"></i> Send
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="footer-section">
                        <small class="text-warning mb-1 d-block">
                            <i class="bi bi-exclamation-triangle"></i> 
                            <strong>Crisis?</strong> Call 988 (Suicide & Crisis Lifeline) or 911 immediately
                        </small>
                        <small class="text-muted">
                            <i class="bi bi-shield-check"></i> 
                            Safe space • 
                            <a href="/webhook-info" class="text-muted">
                                <i class="bi bi-code-slash"></i> Developer info
                            </a>
                        </small>
                    </div>
                </div>
            </div>
        </div>

        <script>
            // Hide loading screen when page is fully loaded
            window.addEventListener('load', function() {
                setTimeout(function() {
                    const loadingScreen = document.getElementById('loadingScreen');
                    loadingScreen.classList.add('hidden');
                    
                    // Remove from DOM after animation completes
                    setTimeout(function() {
                        loadingScreen.style.display = 'none';
                    }, 500);
                }, 1000); // Show loading for at least 1 second for better UX
            });

            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }
            
            function sendQuickMessage(message) {
                document.getElementById('messageInput').value = message;
                sendMessage();
            }
            
            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (!message) return;
                
                // Add user message to chat
                addMessage(message, 'user');
                input.value = '';
                
                // Show typing indicator
                showTyping(true);
                
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: message })
                    });
                    
                    const data = await response.json();
                    
                    // Hide typing indicator
                    showTyping(false);
                    
                    // Add bot response
                    addMessage(data.response, 'bot');
                    
                } catch (error) {
                    showTyping(false);
                    addMessage("I'm having trouble connecting right now. Please try again in a moment.", 'bot');
                }
            }
            
            function addMessage(text, sender) {
                const chatContainer = document.getElementById('chatContainer');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}`;
                
                const avatar = sender === 'user' ? 
                    '<div class="message-avatar"><i class="bi bi-person-circle"></i></div>' :
                    '<div class="message-avatar"><i class="bi bi-robot"></i></div>';
                
                const senderName = sender === 'user' ? 'You' : 'AMIGO';
                
                messageDiv.innerHTML = `
                    ${avatar}
                    <div class="message-content">
                        <strong>${senderName}</strong><br>
                        ${text}
                    </div>
                `;
                
                chatContainer.appendChild(messageDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
            
            function showTyping(show) {
                const typingIndicator = document.getElementById('typingIndicator');
                if (show) {
                    typingIndicator.classList.add('show');
                    typingIndicator.style.display = 'flex';
                } else {
                    typingIndicator.classList.remove('show');
                    typingIndicator.style.display = 'none';
                }
                
                if (show) {
                    const chatContainer = document.getElementById('chatContainer');
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }
            }
        </script>
    </body>
    </html>
    """

@app.route('/webhook-info', methods=['GET'])
def webhook_info():
    """
    Information page for developers wanting to integrate with Dialogflow
    """
    return """
    <!DOCTYPE html>
    <html lang="en" data-bs-theme="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AMIGO - Webhook Integration</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-lg-8">
                    <div class="text-center mb-5">
                        <h1 class="display-4 fw-bold text-primary mb-3">
                            <i class="bi bi-code-slash"></i> AMIGO Webhook
                        </h1>
                        <p class="lead text-muted">Developer Integration Guide</p>
                        <a href="/" class="btn btn-outline-primary">
                            <i class="bi bi-arrow-left"></i> Back to Chat Demo
                        </a>
                    </div>
                    
                    <div class="card mb-4">
                        <div class="card-body">
                            <h2 class="card-title h4 mb-3">
                                <i class="bi bi-link-45deg"></i> Webhook Endpoints
                            </h2>
                            <div class="row g-3">
                                <div class="col-md-6">
                                    <div class="p-3 bg-dark rounded">
                                        <strong class="text-success">Main Webhook:</strong><br>
                                        <code class="text-light">/webhook</code><br>
                                        <small class="text-muted">For Dialogflow integration</small>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="p-3 bg-dark rounded">
                                        <strong class="text-info">Health Check:</strong><br>
                                        <code class="text-light">/health</code><br>
                                        <small class="text-muted">Server status monitoring</small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="card mb-4">
                        <div class="card-body">
                            <h3 class="card-title h5 mb-3">
                                <i class="bi bi-gear"></i> Dialogflow Setup
                            </h3>
                            <ol class="list-group list-group-numbered list-group-flush">
                                <li class="list-group-item bg-transparent border-0 px-0">
                                    Copy this webhook URL to your Google Dialogflow agent
                                </li>
                                <li class="list-group-item bg-transparent border-0 px-0">
                                    Navigate to <strong>Fulfillment</strong> in your Dialogflow console
                                </li>
                                <li class="list-group-item bg-transparent border-0 px-0">
                                    Enable webhook and paste the URL with <code>/webhook</code> endpoint
                                </li>
                                <li class="list-group-item bg-transparent border-0 px-0">
                                    Configure your intents to use webhook fulfillment
                                </li>
                            </ol>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-body">
                            <h3 class="card-title h5 mb-3">
                                <i class="bi bi-code"></i> Sample Test Request
                            </h3>
                            <p class="text-muted">Use this curl command to test the webhook:</p>
                            <pre class="bg-dark p-3 rounded"><code class="text-light">curl -X POST [YOUR_WEBHOOK_URL]/webhook \\
  -H "Content-Type: application/json" \\
  -d '{
    "queryResult": {
      "intent": {
        "displayName": "express_sadness"
      },
      "queryText": "I feel really sad today",
      "parameters": {}
    },
    "session": "projects/test-project/agent/sessions/test-session"
  }'</code></pre>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
