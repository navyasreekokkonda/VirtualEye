import time
import random
import pyttsx3  # Text-to-speech

# --- Distance Configuration ---
MAX_DISTANCE_FOR_ALERT = 50  # cm
MIN_DELAY_SEC = 0.5          # Minimum interval between voice alerts

# --- Initialize pyttsx3 ---
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speech speed (default ~200)
engine.setProperty('volume', 1.0)  # Volume 0.0 to 1.0

# --- Function to simulate distance readings ---
def get_distance():
    """
    Replace this function with actual sensor reading on Raspberry Pi:
    
    # GPIO.output(TRIG, True)
    # time.sleep(0.00001)
    # GPIO.output(TRIG, False)
    # ... measure pulse ...
    # return distance_cm
    """
    return round(random.uniform(10, 100), 2)  # Simulated distance

# --- Function to speak obstacle alert ---
def speak_alert(distance_cm):
    if distance_cm < MAX_DISTANCE_FOR_ALERT:
        msg = f"Warning! Obstacle {distance_cm:.0f} centimeters ahead."
        engine.say(msg)
        engine.runAndWait()

# --- Main Loop ---
last_alert_time = 0

try:
    print("\n--- Distance Alert with Voice (pyttsx3) ---")
    print(f"Voice alert active if distance < {MAX_DISTANCE_FOR_ALERT} cm.")
    print("Press Ctrl+C to stop.\n")

    while True:
        dist = get_distance()
        print(f"Distance: {dist:.2f} cm", end='\r')

        current_time = time.time()
        if dist < MAX_DISTANCE_FOR_ALERT and current_time - last_alert_time > MIN_DELAY_SEC:
            speak_alert(dist)
            last_alert_time = current_time

        time.sleep(0.1)  # Small delay to avoid tight loop

except KeyboardInterrupt:
    print("\nStopped by user.")
