import cv2
import time
from speech_module import speak

def safe_read(cam):
    try:
        ret, frame = cam.read()
        if not ret or frame is None:
            return None
        return cv2.resize(frame, (640, 480))
    except:
        return None

def side_camera_detection(detector, phone_ip):
    while True:
        side_cam = cv2.VideoCapture(phone_ip)
        if not side_cam.isOpened():
            print("❌ ERROR: Could not open side camera. Retrying in 2s...")
            time.sleep(2)
            continue

        while True:
            frame = safe_read(side_cam)
            if frame is None:
                time.sleep(0.05)
                continue

            results, frame = detector.detect(frame)

            for obj in results:
                x, y, w, h = obj.get("bbox", (0,0,0,0))
                if None not in (x, y, w, h):
                    cv2.rectangle(frame, (int(x), int(y)), (int(x+w), int(y+h)), (0,255,0), 2)
                    speak(f"I see a {obj['label']}", cam="side")

            cv2.imshow("Side Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                side_cam.release()
                cv2.destroyWindow("Side Camera")
                break

        side_cam.release()
