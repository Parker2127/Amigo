import logging
import random
from responses import get_response_variants, get_coping_strategies, get_validation_responses

def handle_intent(intent_name, parameters, query_text, session_id, input_contexts):
    """
    Main intent router that dispatches to appropriate handler functions
    
    Args:
        intent_name (str): The display name of the triggered intent
        parameters (dict): Extracted parameters from user input
        query_text (str): Original user query
        session_id (str): Unique session identifier
        input_contexts (list): Current conversation contexts
    
    Returns:
        dict: Response data including text and optional contexts
    """
    
    logging.info(f"Handling intent: {intent_name}")
    
    # Intent mapping to handler functions
    intent_handlers = {
        'Default Welcome Intent': handle_greeting,
        'greeting': handle_greeting,
        'positive_wellbeing': handle_positive_wellbeing,
        'express_sadness': handle_express_sadness,
        'express_anxiety': handle_express_anxiety,
        'express_anger': handle_express_anger,
        'ask_coping_strategy': handle_ask_coping_strategy,
        'breathing_exercise': handle_breathing_exercise,
        'grounding_technique': handle_grounding_technique,
        'positive_affirmation': handle_positive_affirmation,
        'check_in': handle_check_in,
        'goodbye': handle_goodbye,
        'Default Fallback Intent': handle_fallback,
        'fallback': handle_fallback
    }
    
    # Get handler function or use fallback
    handler = intent_handlers.get(intent_name, handle_fallback)
    
    # Call the appropriate handler
    return handler(parameters, query_text, session_id, input_contexts)

def handle_greeting(parameters, query_text, session_id, input_contexts):
    """Handle greeting intents with warm, welcoming responses"""
    
    responses = get_response_variants('greeting')
    response_text = random.choice(responses)
    
    # Set context for ongoing conversation
    output_contexts = [{
        "name": f"projects/your-project/agent/sessions/{session_id}/contexts/conversation-started",
        "lifespanCount": 5,
        "parameters": {
            "greeting_given": True
        }
    }]
    
    return {
        'text': response_text,
        'output_contexts': output_contexts
    }

def handle_positive_wellbeing(parameters, query_text, session_id, input_contexts):
    """Handle positive emotional expressions with celebratory and supportive responses"""
    
    positive_responses = [
        "That's wonderful to hear! I'm so glad you're feeling good today. It's important to celebrate these positive moments. Is there anything that's particularly contributing to your good mood?",
        "I'm really happy to hear you're doing well! These positive feelings are precious. What's been going well for you lately?",
        "That's fantastic! It's great that you're feeling good. Sometimes sharing our positive moments can make them even brighter. What's bringing you joy today?",
        "I love hearing that you're feeling good! It's wonderful when we can recognize and appreciate these positive emotions. Is there anything specific that's making today good for you?",
        "That's so great to hear! Your positive energy comes through even in text. It's beautiful when we can acknowledge our good moments. What would you like to talk about while you're feeling this way?"
    ]
    
    follow_up_questions = [
        "Would you like to share what's been going well?",
        "Is there anything you'd like to celebrate or talk about?",
        "I'm here if you want to share more about your good day!",
        "What's been the highlight of your day so far?"
    ]
    
    response = random.choice(positive_responses)
    
    # Sometimes add a follow-up question
    if random.choice([True, False]):
        follow_up = random.choice(follow_up_questions)
        response += f" {follow_up}"
    
    return {
        'text': response,
        'output_contexts': []
    }

def handle_express_sadness(parameters, query_text, session_id, input_contexts):
    """Handle expressions of sadness with empathetic validation"""
    
    # More human, conversational sadness responses
    human_sadness_responses = [
        "Oh, I'm really sorry you're feeling sad right now. That sounds really tough. You know, it takes a lot of courage to share that with me. What's been weighing on your heart?",
        "I can hear the sadness in your words, and I just want you to know that what you're feeling is so valid. Sometimes life just hits us hard, doesn't it? Want to tell me what's been going on?",
        "Aw, I'm sorry you're going through this. Sadness can feel so heavy sometimes. I'm really glad you reached out though - that shows strength. What's been making things difficult lately?",
        "I feel for you, I really do. It sounds like you're carrying something heavy right now. You don't have to carry it alone though. What's been on your mind?",
        "That sounds really hard. I can sense you're hurting, and I want you to know I'm here with you in this moment. Sometimes it just helps to have someone listen, you know? What's been making you feel this way?"
    ]
    
    response_text = random.choice(human_sadness_responses)
    
    # Set emotional context
    output_contexts = [{
        "name": f"projects/your-project/agent/sessions/{session_id}/contexts/emotional-state",
        "lifespanCount": 10,
        "parameters": {
            "emotion": "sadness",
            "support_offered": True
        }
    }]
    
    return {
        'text': response_text,
        'output_contexts': output_contexts
    }

def handle_express_anxiety(parameters, query_text, session_id, input_contexts):
    """Handle expressions of anxiety with calming validation"""
    
    # More natural, human anxiety responses
    human_anxiety_responses = [
        "Oh no, anxiety can be so overwhelming. I totally get that - it's like your mind just won't stop racing, right? You're not alone in this feeling. What's been making you feel anxious today?",
        "Ugh, anxiety is the worst. It can make everything feel so much bigger and scarier than it actually is. I'm really glad you're talking about it though. What's been on your mind that's got you feeling worried?",
        "I hear you on the anxiety - it can be such a tough feeling to sit with. Sometimes it feels like it just takes over everything, doesn't it? I'm here to help you work through this. What's been triggering these feelings?",
        "Anxiety can be so exhausting, both mentally and physically. I really feel for you right now. You know what though? Reaching out like this is actually a really healthy way to handle it. What's been causing these anxious feelings?",
        "Oh, I'm sorry you're dealing with anxiety. It can make even simple things feel impossible sometimes. But hey, you're here talking about it, which is honestly really brave. What's been making you feel this way?"
    ]
    
    response_text = random.choice(human_anxiety_responses)
    
    output_contexts = [{
        "name": f"projects/your-project/agent/sessions/{session_id}/contexts/emotional-state",
        "lifespanCount": 10,
        "parameters": {
            "emotion": "anxiety",
            "coping_suggested": False
        }
    }]
    
    return {
        'text': response_text,
        'output_contexts': output_contexts
    }

def handle_express_anger(parameters, query_text, session_id, input_contexts):
    """Handle expressions of anger with understanding validation"""
    
    validation_responses = get_validation_responses('anger')
    validation = random.choice(validation_responses)
    
    followup_questions = [
        "What happened that made you feel this way?",
        "It sounds like something really frustrated you. Would you like to share what happened?",
        "Anger often comes from feeling hurt or misunderstood. What's behind these feelings?",
        "I can hear that you're upset. What would help you feel better right now?"
    ]
    
    followup = random.choice(followup_questions)
    response_text = f"{validation} {followup}"
    
    output_contexts = [{
        "name": f"projects/your-project/agent/sessions/{session_id}/contexts/emotional-state",
        "lifespanCount": 10,
        "parameters": {
            "emotion": "anger",
            "validation_given": True
        }
    }]
    
    return {
        'text': response_text,
        'output_contexts': output_contexts
    }

def handle_ask_coping_strategy(parameters, query_text, session_id, input_contexts):
    """Provide coping strategies based on context and user needs"""
    
    strategies = get_coping_strategies()
    strategy = random.choice(strategies)
    
    intro_phrases = [
        "Here's something that might help:",
        "Let's try this together:",
        "This technique has helped many people:",
        "I'd like to suggest something that might be helpful:"
    ]
    
    intro = random.choice(intro_phrases)
    response_text = f"{intro} {strategy}"
    
    output_contexts = [{
        "name": f"projects/your-project/agent/sessions/{session_id}/contexts/coping-strategy",
        "lifespanCount": 5,
        "parameters": {
            "strategy_provided": True,
            "strategy_type": "general"
        }
    }]
    
    return {
        'text': response_text,
        'output_contexts': output_contexts
    }

def handle_breathing_exercise(parameters, query_text, session_id, input_contexts):
    """Guide user through breathing exercises"""
    
    # More conversational breathing exercises
    conversational_breathing = [
        "Absolutely! Breathing exercises are amazing - they're like a reset button for your nervous system. Let's do the 4-7-8 technique together. It might feel a bit weird at first, but trust me on this one. Ready? Breathe in through your nose for 4... hold it for 7... and out through your mouth for 8. You're doing great! Want to try that a couple more times?",
        "Great idea! I love box breathing - it's so simple but really effective. Think of it like drawing a square with your breath. Breathe in for 4 counts, hold for 4, out for 4, hold for 4. Let's do it together: In... 2... 3... 4... Hold... 2... 3... 4... Out... 2... 3... 4... Hold... 2... 3... 4. How does that feel?",
        "Perfect choice! Here's one of my favorites - belly breathing. It's super simple but really powerful. Put one hand on your chest, one on your belly. When you breathe in through your nose, try to make only your belly hand move, not the chest one. Then breathe out slowly through your mouth. It tells your body 'hey, everything's okay' and activates that natural relaxation response. Give it a try!"
    ]
    
    response_text = random.choice(conversational_breathing)
    
    output_contexts = [{
        "name": f"projects/your-project/agent/sessions/{session_id}/contexts/coping-strategy",
        "lifespanCount": 5,
        "parameters": {
            "strategy_provided": True,
            "strategy_type": "breathing"
        }
    }]
    
    return {
        'text': response_text,
        'output_contexts': output_contexts
    }

def handle_grounding_technique(parameters, query_text, session_id, input_contexts):
    """Provide grounding techniques for anxiety and overwhelm"""
    
    grounding_techniques = [
        "Let's try the 5-4-3-2-1 grounding technique. Look around and name: 5 things you can see, 4 things you can touch, 3 things you can hear, 2 things you can smell, and 1 thing you can taste. This helps bring you back to the present moment.",
        "Here's a grounding exercise: Put your feet flat on the floor and really feel them touching the ground. Take three deep breaths. Now notice the temperature of the air on your skin. You're safe here in this moment.",
        "Try this grounding technique: Hold an object near you - your phone, a cup, anything. Focus on how it feels - its weight, texture, temperature. Describe it to yourself in detail. This helps anchor you to the present."
    ]
    
    response_text = random.choice(grounding_techniques)
    
    output_contexts = [{
        "name": f"projects/your-project/agent/sessions/{session_id}/contexts/coping-strategy",
        "lifespanCount": 5,
        "parameters": {
            "strategy_provided": True,
            "strategy_type": "grounding"
        }
    }]
    
    return {
        'text': response_text,
        'output_contexts': output_contexts
    }

def handle_positive_affirmation(parameters, query_text, session_id, input_contexts):
    """Provide positive affirmations and self-compassion exercises"""
    
    affirmations = [
        "Remember: You are worthy of love and kindness, especially from yourself. Your feelings are valid, and it's okay to have difficult moments. You're doing the best you can with what you have right now.",
        "Here's a gentle reminder: You have survived 100% of your difficult days so far. You are stronger than you know, and this feeling will pass. Be patient and gentle with yourself.",
        "Let's practice some self-compassion: Place your hand on your heart and say to yourself, 'May I be kind to myself. May I give myself the compassion I need. May I be strong and patient.' You deserve the same kindness you'd give a good friend."
    ]
    
    response_text = random.choice(affirmations)
    
    return {
        'text': response_text,
        'output_contexts': []
    }

def handle_check_in(parameters, query_text, session_id, input_contexts):
    """Handle check-ins in a more human, conversational way"""
    
    # Detect if user is asking about AMIGO's wellbeing
    if any(phrase in query_text.lower() for phrase in ['how are you', 'how you doing', 'how you been', 'how\'s it going']):
        # Respond like a human would, then redirect caringly to user
        human_responses = [
            "I'm doing well, thank you for asking! I feel fulfilled when I can be here for people like you. Speaking of which, how are you doing today? Is there anything on your mind?",
            "I'm good! I genuinely enjoy our conversations and being able to support people. It means a lot to me. How about you - how are you feeling today?",
            "I'm doing great, thanks! I feel energized when I can help and listen. I appreciate you asking! Now, how are you doing? What's been on your heart lately?",
            "I'm well! I find purpose in these conversations and being present for people. Thanks for checking in on me! How are you feeling today? Is there anything you'd like to talk about?",
            "I'm doing really good! There's something special about connecting with people and being able to offer support. I appreciate you asking! How about you - what's going on in your world today?"
        ]
        
        response_text = random.choice(human_responses)
    else:
        # User isn't asking about AMIGO specifically, so check in on them
        checkin_responses = [
            "How are you feeling right now? I'm here to listen and support you through whatever you're experiencing.",
            "What's been on your mind lately? Remember, there's no pressure to share more than you're comfortable with.",
            "How has your day been treating you? I'm here if you need someone to talk to or just want to share how you're doing.",
            "I'm curious about how you're doing. What would be most helpful for you right now - talking through something, learning a coping technique, or just having someone listen?"
        ]
        
        response_text = random.choice(checkin_responses)
    
    return {
        'text': response_text,
        'output_contexts': []
    }

def handle_goodbye(parameters, query_text, session_id, input_contexts):
    """Handle farewell with supportive closing"""
    
    goodbye_responses = [
        "Take care of yourself, and remember that I'm here whenever you need support. You're stronger than you know. Until we talk again! 💙",
        "It was good talking with you today. Remember to be gentle with yourself, and don't hesitate to reach out whenever you need someone to listen. Take care! 💙",
        "Thank you for sharing with me today. You're doing great work by taking care of your mental health. I'm here whenever you need me. Be well! 💙",
        "Goodbye for now. Remember: you matter, your feelings are valid, and you deserve kindness - especially from yourself. I'll be here when you're ready to talk again. 💙"
    ]
    
    response_text = random.choice(goodbye_responses)
    
    return {
        'text': response_text,
        'output_contexts': []
    }

def handle_fallback(parameters, query_text, session_id, input_contexts):
    """Handle unrecognized intents with graceful responses"""
    
    # More human, humble fallback responses
    human_fallback_responses = [
        "You know what? I'm not entirely sure I caught what you meant there, but I definitely want to understand. Could you help me out and tell me a bit more about what you're feeling or what's on your mind?",
        "Hmm, I think I might have missed something there. I'm still learning how to pick up on all the nuances of what people share with me. Can you help me understand what you're going through right now?",
        "I'm going to be honest - I'm not quite sure how to respond to that, but I can tell you might need someone to talk to. What would be most helpful for you right now? I'm here to listen.",
        "You know, sometimes I don't catch everything perfectly, but I really want to be here for you. Could you tell me more about what's on your heart or what kind of support you're looking for today?",
        "I feel like I might have missed the mark there. I'm still figuring out how to be the best listener I can be. Would you mind sharing a bit more about what you're experiencing right now?"
    ]
    
    response_text = random.choice(human_fallback_responses)
    
    output_contexts = [{
        "name": f"projects/your-project/agent/sessions/{session_id}/contexts/clarification-needed",
        "lifespanCount": 3,
        "parameters": {
            "fallback_triggered": True,
            "original_query": query_text
        }
    }]
    
    return {
        'text': response_text,
        'output_contexts': output_contexts
    }
