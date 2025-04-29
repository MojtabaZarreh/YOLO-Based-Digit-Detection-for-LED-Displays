import cv2
import numpy as np
from utils.image_ops import ImageProcessor
from conf.config import CAMERA_URL
import numpy as np

rectangles = [
    {"x": 325, "y": 0, "width": 250, "height": 600}, 
    {"x": 0, "y": 150, "width": 1000, "height": 200},
    {"x": 0, "y": 0, "width": 800, "height": 100},
    {"x": 0, "y": 60, "width": 220, "height": 150},  
]

def apply_masks(image, rectangles):
    if image is None or image.size == 0:
        print("Input image is empty or invalid.")
        return image

    masked_image = image.copy()
    for rect in rectangles:
        x, y, width, height = rect["x"], rect["y"], rect["width"], rect["height"]
        x1, y1 = x, y
        x2, y2 = x + width, y + height
        cv2.rectangle(masked_image, (x1, y1), (x2, y2), (0, 0, 0), thickness=-1)
    return masked_image

def enhance_display_area(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
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

def test_crop_image():
    cap = cv2.VideoCapture(CAMERA_URL)
    if not cap.isOpened():
        print("Unable to access camera")
        return

    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        cap.release()
        return

    cropper = ImageProcessor(crop_region=(700, 120, 1250, 450)) 
    cropped_image = cropper.crop_image(frame)
    enhanced_image = enhance_display_area(cropped_image)
    masked_frame = apply_masks(enhanced_image, rectangles)

    cv2.imwrite("cropped_image.jpg", masked_frame)
    print("Saved cropped_image.jpg")

if __name__ == "__main__":
    test_crop_image()