import cv2
import numpy as np 

class IPCamera:
    def __init__(self, url: str) -> None:
        self.url = url
        
    def capture_frame(self) -> np.ndarray:
        cap = cv2.VideoCapture(self.url)
        if not cap.isOpened():
            raise RuntimeError("Cannot open camera stream.")
        ret, frame = cap.read()
        cap.release()
        if not ret:
            raise RuntimeError("Failed to capture frame.")
        return frame