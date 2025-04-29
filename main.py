import os
from conf.config import *
import cv2
from camera.ip_camera import IPCamera
from detector.model_api import RoboflowClient
from utils.image_ops import ImageProcessor
from utils.sms_sender import SMSSender
from utils.temperature_analysis import first_order_difference
from scheduler.job_scheduler import JobScheduler
import numpy as np
from database.db import Database

class ModelPipeline:
    global_counter = 0
    def __init__(self, camera_url: str, model_url: str, api_key: str, crop_region: tuple[int, int, int, int], interval_seconds: int):
        self.camera = IPCamera(camera_url)
        self.detector = RoboflowClient(model_url, api_key, LOCAL_MODEL, CONFIDENCE, OVERLAP)
        self.processor = ImageProcessor(crop_region)
        self.scheduler = JobScheduler(interval_seconds, self.process_and_annotate)
        
    def save_image(self, image):
        output_path = os.path.join(OUTPUT_DIR, f"annotated_frame.jpg")
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        cv2.imwrite(output_path, image)
        
    def capture_frame(self):
        return self.camera.capture_frame()
        
    def predict(self, image_path: str):
        # result = self.detector.predict(image_path)['predictions']
        result = self.detector.predict_local(image_path)

        sorted_classes = sorted(result, key=lambda d: d['x'])
        temp_str = ''.join(str(int(det['class_id'])) for det in sorted_classes)[:3]

        if not temp_str:
            print("No temperature digits detected.")
            return result

        decimal_temp = float(f"{temp_str[:-1]}.{temp_str[-1]}") if len(temp_str) >= 2 else float(temp_str)
        rounded_temp = round(decimal_temp)

        print(f"Raw: {temp_str} | Decimal: {decimal_temp} | Rounded: {rounded_temp}")

        db = Database()
        last_temp = db.get_last_temperature()
        print(f'Last data : {last_temp[1]}, {last_temp[0]}°')

        if last_temp is None:
            print("No previous temperature found. Inserting new record.")
        elif abs(rounded_temp - last_temp[0]) > 4:
            print(f"Skipped: ΔTemp = {abs(rounded_temp - last_temp[0])}° > 5° (Last: {last_temp[0]}, New: {rounded_temp})")
            return result

        db.insert_records_to_database(rounded_temp)
        ModelPipeline.global_counter += 1
        if rounded_temp > 25.0:
            SMSSender.send_alert(last_temp[1])
        return result

    def annotate_image(self, image: np.ndarray, predictions: list) -> np.ndarray:
        return self.processor.annotate_image(image, predictions)
        
    def process_and_annotate(self):
        raw_frame = self.capture_frame()
        masked_frame = self.processor.masked_image(self.processor.crop_image(raw_frame))
        temp_path = os.path.join(OUTPUT_DIR, f"frame.jpg")
        cv2.imwrite(temp_path, masked_frame)

        predictions = self.predict(temp_path)
        annotated_image = self.annotate_image(masked_frame, predictions)
        self.save_image(annotated_image)
        print(f'Counter status : {ModelPipeline.global_counter}\n')
        if ModelPipeline.global_counter == 6:
            if first_order_difference(Database().get_5_temperature()):
                print('The temperature process is increasing !\n')
                SMSSender.send_alert(0)
            ModelPipeline.global_counter = 0

    def start(self):
        self.scheduler.start()

def main():
    pipeline = ModelPipeline(CAMERA_URL, 
                             MODEL_URL, 
                             API_KEY, 
                             CROP_REGION, 
                             CAPTURE_INTERVAL_SECONDS)
    pipeline.start()

if __name__ == "__main__":
    main()