import requests
from ultralytics import YOLO
import uuid

class RoboflowClient:
    def __init__(self, model_url: str, api_key: str, local_model_path: str,
                 confidence: int = 40, overlap: int = 30):
        self.model_url = model_url
        self.api_key = api_key
        self.confidence = confidence
        self.overlap = overlap
        self.local_model_path = local_model_path
        self.local_model = YOLO(local_model_path) if local_model_path else None

    def predict(self, image_path: str) -> dict:
        with open(image_path, "rb") as image_file:
            response = requests.post(
                self.model_url,
                params={
                    "api_key": self.api_key,
                    "confidence": self.confidence,
                    "overlap": self.overlap
                },
                files={"file": image_file}
            )
        return response.json()
    
    def predict_local(self, image_path: str) -> list:
        results = self.local_model(image_path)
        detections = results[0].boxes

        formatted = []
        for box in detections:
            x_center, y_center, w, h = box.xywh[0].tolist()  
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = self.local_model.names[class_id]  

            formatted.append({
                'x': x_center,
                'y': y_center,
                'width': w,
                'height': h,
                'confidence': confidence,
                'class': class_name,
                'class_id': class_id,
                'detection_id': str(uuid.uuid4()) 
            })

        return formatted