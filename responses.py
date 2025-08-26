"""
Response content for AMIGO therapy chatbot
Organized by intent type for easy modification and expansion
"""

def get_response_variants(intent_type):
    """
    Get response variations for different intent types
    
    Args:
        intent_type (str): The type of intent (greeting, goodbye, etc.)
    
    Returns:
        list: List of response variations
    """
    
    responses = {
        'greeting': [
            "Hello! I'm AMIGO, and I'm here to listen and support you. How are you feeling today?",
            "Hi there! I'm glad you're here. My name is AMIGO, and I'm here to provide a safe space for you to share what's on your mind. How can I support you today?",
            "Welcome! I'm AMIGO, your compassionate AI companion. I'm here to listen without judgment and help you work through whatever you're experiencing. What's on your heart today?",
            "Hello, and thank you for reaching out. I'm AMIGO, and I care about your wellbeing. This is a safe space where you can share your thoughts and feelings. How are you doing right now?",
            "Hi! I'm AMIGO, here to offer support and understanding. I'm glad you decided to connect today. What would you like to talk about?"
        ]
    }
    
    return responses.get(intent_type, ["I'm here to help. How can I support you today?"])

def get_validation_responses(emotion_type):
    """
    Get empathetic validation responses for different emotions
    
    Args:
        emotion_type (str): The emotion being expressed (sadness, anxiety, anger, etc.)
    
    Returns:
        list: List of validation responses
    """
    
    validations = {
        'sadness': [
            "I can hear the sadness in your words, and I want you to know that what you're feeling is completely valid.",
            "It sounds like you're going through a really difficult time. Your feelings of sadness are important and deserving of attention.",
            "I'm sorry you're experiencing this sadness. It takes courage to acknowledge and share these feelings.",
            "Thank you for trusting me with your feelings. Sadness is a natural part of the human experience, and you're not alone in feeling this way.",
            "I can sense the weight of what you're carrying. Your sadness is real and valid, and I'm here to support you through this."
        ],
        'anxiety': [
            "I understand that you're feeling anxious, and I want you to know that anxiety is a very real and challenging experience.",
            "It sounds like anxiety is making things feel overwhelming right now. These feelings are valid and you're not alone.",
            "I hear that you're struggling with anxious feelings. Anxiety can be incredibly difficult to manage, and I'm here to help.",
            "Thank you for sharing what you're experiencing. Anxiety affects so many people, and what you're feeling is completely understandable.",
            "I can sense that anxiety is weighing on you. These feelings are real and important, and together we can work through them."
        ],
        'anger': [
            "I can hear that you're feeling angry, and those feelings are completely valid. Anger often tells us something important.",
            "It sounds like something has really upset you. Your anger is a natural response, and it's okay to feel this way.",
            "I understand that you're experiencing anger right now. These feelings deserve to be acknowledged and respected.",
            "Thank you for sharing these difficult feelings with me. Anger can be a powerful emotion, and it's important to honor what you're experiencing.",
            "I can sense the frustration and anger you're feeling. These emotions are part of being human, and you have every right to feel them."
        ],
        'stress': [
            "It sounds like you're under a lot of stress right now. These feelings of being overwhelmed are completely understandable.",
            "I can hear that stress is taking a toll on you. What you're experiencing is real and significant.",
            "Stress can feel so overwhelming. I want you to know that what you're going through is valid and you don't have to handle it alone.",
            "I understand that you're feeling stressed. This is such a common human experience, and your feelings about it are important.",
            "It sounds like there's a lot on your plate right now. Feeling stressed under these circumstances makes complete sense."
        ]
    }
    
    return validations.get(emotion_type, [
        "I can hear that you're going through something difficult right now, and I want you to know that your feelings are valid and important."
    ])

def get_coping_strategies():
    """
    Get a variety of coping strategies for different situations
    
    Returns:
        list: List of coping strategies
    """
    
    strategies = [
        "Try the 'STOP' technique: Stop what you're doing, Take a breath, Observe your thoughts and feelings without judgment, and then Proceed with intention. This can help create space between you and overwhelming emotions.",
        
        "Practice progressive muscle relaxation: Start with your toes and work your way up, tensing each muscle group for 5 seconds, then releasing. Notice how the tension melts away as you let go.",
        
        "Use the 'name it to tame it' approach: Simply naming what you're feeling (like 'I notice I'm feeling anxious') can help reduce the intensity of the emotion by engaging the rational part of your brain.",
        
        "Try journaling for 5-10 minutes. Write down everything you're thinking and feeling without worrying about grammar or making sense. Sometimes getting thoughts out of your head and onto paper can bring relief.",
        
        "Practice the 'gentle rain' visualization: Imagine your difficult emotions as clouds passing through the sky of your mind. Like weather, emotions are temporary - they come and go naturally.",
        
        "Create a 'comfort kit' - gather small items that bring you peace, like a soft blanket, calming music, tea, or photos that make you smile. Use these when you need comfort.",
        
        "Try the 'one thing' approach: When feeling overwhelmed, focus on just one small thing you can do right now. It could be drinking a glass of water, taking three deep breaths, or organizing one small area.",
        
        "Practice self-compassion by asking yourself: 'What would I say to a good friend going through this?' Then offer yourself that same kindness and understanding.",
        
        "Use the 'time travel' technique: Remind yourself of a time when you felt capable and strong. You've overcome challenges before, and you have that same strength within you now.",
        
        "Try the 'worry window' technique: Set aside 15 minutes each day to worry intentionally. When worries come up outside this time, remind yourself to save them for your worry window."
    ]
    
    return strategies

def get_followup_questions(context):
    """
    Get contextual follow-up questions to continue therapeutic conversation
    
    Args:
        context (str): The conversation context or previous topic
    
    Returns:
        list: List of appropriate follow-up questions
    """
    
    questions = {
        'general': [
            "What feels most important for you to talk about right now?",
            "How would you like me to support you today?",
            "What's been weighing on your mind lately?",
            "Is there something specific that brought you here today?"
        ],
        'emotional': [
            "How long have you been feeling this way?",
            "What do you think might have triggered these feelings?",
            "Have you experienced something like this before?",
            "What would help you feel even a little bit better right now?"
        ],
        'coping': [
            "How did that technique feel for you?",
            "Would you like to try another approach?",
            "What coping strategies have helped you in the past?",
            "Is there anything else you'd like to explore together?"
        ]
    }
    
    return questions.get(context, questions['general'])

def get_crisis_resources():
    """
    Get crisis intervention resources and helpline information
    
    Returns:
        dict: Crisis resources organized by type
    """
    
    return {
        'immediate_danger': {
            'text': "If you're in immediate danger or having thoughts of hurting yourself or others, please reach out for help right away:",
            'resources': [
                "Call 911 (Emergency Services)",
                "Call 988 (Suicide & Crisis Lifeline)",
                "Text HOME to 741741 (Crisis Text Line)",
                "Go to your nearest emergency room"
            ]
        },
        'mental_health_support': {
            'text': "Here are some additional mental health resources:",
            'resources': [
                "National Suicide Prevention Lifeline: 988",
                "Crisis Text Line: Text HOME to 741741",
                "NAMI Helpline: 1-800-950-NAMI (6264)",
                "SAMHSA Helpline: 1-800-662-4357"
            ]
        },
        'specialized_support': {
            'text': "For specialized support:",
            'resources': [
                "National Domestic Violence Hotline: 1-800-799-7233",
                "RAINN Sexual Assault Hotline: 1-800-656-4673",
                "Trans Lifeline: 877-565-8860",
                "LGBT National Hotline: 1-888-843-4564"
            ]
        }
    }

def get_encouraging_phrases():
    """
    Get encouraging phrases for difficult moments
    
    Returns:
        list: List of encouraging phrases
    """
    
    return [
        "You are stronger than you know.",
        "This feeling will pass, even though it's hard right now.",
        "You matter, and your life has value.",
        "It's okay to not be okay sometimes.",
        "You're doing the best you can with what you have.",
        "Taking care of your mental health is brave and important.",
        "You deserve kindness, especially from yourself.",
        "Every small step forward counts.",
        "You've survived difficult times before, and you can get through this too.",
        "You don't have to face this alone."
    ]
