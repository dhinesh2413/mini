import random
import speech_recognition as sr
import pyttsx3
import json
from textblob import TextBlob
from googletrans import Translator

# Initialize text-to-speech engine
engine = pyttsx3.init()
translator = Translator()

# Memory system to store past conversations
memory = []

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    """Convert speech to text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            user_input = recognizer.recognize_google(audio)
            print(f"You said: {user_input}")
            return user_input
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand. Could you repeat that?"
        except sr.RequestError:
            return "Speech recognition service is not available right now."

def get_user_input():
    """Get user input either via text or voice"""
    choice = input("Do you want to type or speak? (type/speak): ").strip().lower()
    if choice == "type":
        return input("You: ")
    else:
        return recognize_speech()

def analyze_sentiment(user_input):
    """Analyze sentiment of user input using TextBlob"""
    analysis = TextBlob(user_input)
    if analysis.sentiment.polarity > 0.2:
        return "positive"
    elif analysis.sentiment.polarity < -0.2:
        return "negative"
    else:
        return "neutral"

def therapist_response(emotion):
    """Generate therapist-like response based on emotion"""
    responses = {
        "positive": [
            "That's great to hear! What made you feel this way?",
            "I'm happy for you! Tell me more about it.",
            "Keep up the positivity! What’s been working well for you?"
        ],
        "neutral": [
            "I see. Could you elaborate on that?",
            "That sounds interesting. Can you tell me more?",
            "Would you like to talk more about this?"
        ],
        "negative": [
            "I'm here for you. Want to talk more about what's bothering you?",
            "That sounds tough. How are you coping with it?",
            "I understand. Would you like some guided relaxation techniques?"
        ]
    }
    return random.choice(responses[emotion])

def guided_relaxation():
    """Provides a simple relaxation technique"""
    exercises = [
        "Take a deep breath in... hold for 5 seconds... and slowly exhale.",
        "Try closing your eyes and thinking of a happy memory for a moment.",
        "Let's do a quick grounding exercise: Name 3 things you can see, 2 things you can hear, and 1 thing you can feel."
    ]
    return random.choice(exercises)

def translate_text(text, target_language):
    """Translate text to the target language"""
    try:
        translated = translator.translate(text, dest=target_language)
        return translated.text
    except Exception as e:
        return "Translation error."

def chatbot():
    print("Hello! I'm your AI therapist. How are you feeling today?")
    speak("Hello! I'm your AI therapist. How are you feeling today?")
    while True:
        user_input = get_user_input()
        if user_input.lower() in ["bye", "exit", "quit"]:
            print("Therapist: Take care! I'm always here if you need to talk.")
            speak("Take care! I'm always here if you need to talk.")
            break
        
        memory.append(user_input)  # Store conversation history
        emotion = analyze_sentiment(user_input)
        response = therapist_response(emotion)
        print(f"Therapist: {response}")
        speak(response)
        
        if emotion == "negative":
            relaxation_tip = guided_relaxation()
            print(f"Therapist: {relaxation_tip}")
            speak(relaxation_tip)

if __name__ == "__main__":
    chatbot()