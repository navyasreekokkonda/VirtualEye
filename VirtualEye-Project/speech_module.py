import pyttsx3
import threading

speech_lock = threading.Lock()

def speak(text, cam="front"):
    with speech_lock:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.setProperty("volume", 1.0)
        print(f"🗣 [{cam}] Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
