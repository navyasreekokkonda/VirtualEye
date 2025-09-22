import cv2
import os

class YOLODetector:
    def __init__(self, cfg_path, weights_path, names_path):
        for path in [cfg_path, weights_path, names_path]:
            if not os.path.exists(path):
                raise FileNotFoundError(f"❌ YOLO file not found: {path}")

        with open(names_path, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

        self.net = cv2.dnn.readNet(cfg_path, weights_path)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        unconnected = self.net.getUnconnectedOutLayers()
        layer_names = self.net.getLayerNames()
        if len(unconnected.shape) == 2:
            self.output_layers = [layer_names[i[0]-1] for i in unconnected]
        else:
            self.output_layers = [layer_names[i-1] for i in unconnected]

    def detect(self, frame, conf_threshold=0.6, nms_threshold=0.4):
        height, width = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416,416), swapRB=True, crop=False)
        self.net.setInput(blob)
        outputs = self.net.forward(self.output_layers)

        class_ids, confidences, boxes = [], [], []
        for out in outputs:
            for detection in out:
                scores = detection[5:]
                class_id = int(scores.argmax())
                confidence = scores[class_id]
                if confidence > conf_threshold:
                    center_x = int(detection[0]*width)
                    center_y = int(detection[1]*height)
                    w = int(detection[2]*width)
                    h = int(detection[3]*height)
                    x = int(center_x - w/2)
                    y = int(center_y - h/2)
                    boxes.append([x,y,w,h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
        results = []

        if indices is not None:
            if isinstance(indices, tuple):
                indices = indices[0] if len(indices) > 0 else []
            for i in indices.flatten() if len(indices) > 0 else []:
                results.append({
                    "label": self.classes[class_ids[i]],
                    "confidence": confidences[i],
                    "bbox": boxes[i]
                })

        return results, frame
