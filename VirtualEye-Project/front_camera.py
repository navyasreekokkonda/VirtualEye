import cv2
from speech_module import speak

def safe_read(cam):
    try:
        ret, frame = cam.read()
        if not ret or frame is None:
            return None
        return cv2.resize(frame, (640, 480))
    except:
        return None

def front_camera_detection(detector):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ ERROR: Could not open front camera.")
        return

    while True:
        frame = safe_read(cap)
        if frame is None:
            continue

        results, frame = detector.detect(frame)

        for obj in results:
            x, y, w, h = obj.get("bbox", (0,0,0,0))
            if None not in (x, y, w, h):
                cv2.rectangle(frame, (int(x), int(y)), (int(x+w), int(y+h)), (255,0,0), 2)
                speak(f"I see a {obj['label']}", cam="front")

        cv2.imshow("Front Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyWindow("Front Camera")
