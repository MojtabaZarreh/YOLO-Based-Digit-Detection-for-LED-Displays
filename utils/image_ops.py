import cv2
import numpy as np

class ImageProcessor:
    def __init__(self, crop_region: tuple[int, int, int, int]):
        self.crop_region = crop_region
        self.rectangles = [
                {"x": 325, "y": 0, "width": 250, "height": 600}, 
                {"x": 0, "y": 150, "width": 1000, "height": 200},
                {"x": 0, "y": 0, "width": 800, "height": 100},
                {"x": 0, "y": 60, "width": 220, "height": 150},  
            ]

    def crop_image(self, image: np.ndarray) -> np.ndarray:
        x1, y1, x2, y2 = self.crop_region
        return image[y1:y2, x1:x2]
    
    def masked_image(self, croped_image: np.ndarray) -> np.ndarray:
        if croped_image is None or croped_image.size == 0:
            print("Input image is empty or invalid.")
            return croped_image

        for rect in self.rectangles:
            x, y, width, height = rect["x"], rect["y"], rect["width"], rect["height"]
            x1, y1 = x, y
            x2, y2 = x + width, y + height
            masked_image = cv2.rectangle(croped_image, (x1, y1), (x2, y2), (0, 0, 0), thickness=-1)
        
        lab = cv2.cvtColor(masked_image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8,8))
        cl = clahe.apply(l)
        merged = cv2.merge((cl, a, b))
        enhanced = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened = cv2.filter2D(enhanced, -1, kernel)
        blurred = cv2.GaussianBlur(sharpened, (5, 5), 1)
        black_boost = cv2.convertScaleAbs(blurred, alpha=1.1, beta=-20)
            
        return black_boost
        
    def annotate_image(self, image: np.ndarray, predictions: list) -> np.ndarray:
        for pred in predictions:
            x, y, width, height = pred["x"], pred["y"], pred["width"], pred["height"]
            class_name = pred["class"]

            x1 = int(x - width / 2)
            y1 = int(y - height / 2)
            x2 = int(x + width / 2)
            y2 = int(y + height / 2)

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (36, 255, 12), 2)

        return image
