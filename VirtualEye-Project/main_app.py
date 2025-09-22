import os
import threading
import time
from object_detection import YOLODetector
from front_camera import front_camera_detection
from side_camera import side_camera_detection

if __name__ == "__main__":
    base_path = r"C:\Users\Admin\Desktop\spec"
    cfg_path = os.path.join(base_path, "yolov3-tiny.cfg")
    weights_path = os.path.join(base_path, "yolov3-tiny.weights")
    names_path = os.path.join(base_path, "coco.names")

    detector = YOLODetector(cfg_path, weights_path, names_path)

    phone_ip = "http://192.168.1.5:8080/video"  # Replace with your phone IP

    front_thread = threading.Thread(target=front_camera_detection, args=(detector,), daemon=True)
    side_thread = threading.Thread(target=side_camera_detection, args=(detector, phone_ip), daemon=True)

    front_thread.start()
    side_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Exiting Virtual Eye...")
