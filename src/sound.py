import pyttsx3

def speak_text(text, engine):
    engine.say(text)
    engine.runAndWait()
