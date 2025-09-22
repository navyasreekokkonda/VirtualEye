# test_yolo.py
# Quick script to test detection on a single image
import sys
import cv2
from object_detection import YOLODetector

if len(sys.argv) < 2:
    print("Usage: python test_yolo.py path/to/image.jpg")
    sys.exit(1)

img_path = sys.argv[1]
img = cv2.imread(img_path)
if img is None:
    print("Failed to load image:", img_path)
    sys.exit(1)

detector = YOLODetector()
detections, t = detector.detect(img)
print(f"Inference time: {t:.3f}s, detections: {len(detections)}")
for d in detections:
    print(d['label'], d['confidence'], d['box'])

for d in detections:
    x,y,w,h = d['box']
    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
    cv2.putText(img, f"{d['label']}:{d['confidence']:.2f}", (x, max(y-8,0)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

cv2.imshow("Test", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
