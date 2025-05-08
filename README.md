# 🔢 Industrial 7-Segment Digit Recognition System

At LECA factory, we needed a reliable system to monitor, control, and store critical parameters of certain machines such as amperage and temperature. Some of these values are highly sensitive and require immediate operator notification in case of significant changes.
To address this need, we developed a computer vision system using YOLO, trained on a large dataset containing images of standard digits and industrial 7-segment LED displays.
Using YOLOv8 and training over 120 epochs, we achieved high accuracy in digit recognition and successfully deployed the system in an industrial environment.

![bandicam2025-04-2309-52-51-114-ezgif com-optimize](https://github.com/user-attachments/assets/f6ed69b2-2748-4897-a2bc-30918a9f7eff)

To solve this, we built a **YOLOv8-based digit recognition system** trained on a diverse dataset of segmented digits. The system performs the following:

- Captures and preprocesses LED images from a fixed camera
- Masks irrelevant screen areas and enhances contrast
- Detects digits using YOLOv8
- Checks for upward trends in values using first-order difference
- Sends SMS alerts in critical cases
- Saves data to a database for analysis

## ✨ Features

- 📸 Automated camera image capture every 200 seconds
- 🔍 Masking and enhancement of relevant screen areas
- 🧠 YOLOv8 model for real-time digit detection
- 📊 Trend analysis using first-order difference
- 📲 SMS alerts to operators on critical changes
- 💾 Database logging for all read values

## 📦 Tech Stack

- OpenCV (image processing)
- YOLOv8 (digit detection)
- Threading/Timer (job scheduling)
- SMS API 
- SQLServer

## 📈 First-Order Difference (Trend Detection)

To detect rising trends in numeric values, we use a discrete approximation of the **first-order derivative**:

### Mathematical Formulation

Given a sequence of values \( x_0, x_1, x_2, \dots, x_n \), the first-order difference is defined as:

\[
\Delta x_i = x_{i+1} - x_i
\]

We then calculate the ratio of positive steps (i.e., steps where \( \Delta x_i > 0 \)):

\[
\text{positive\_ratio} = \frac{\text{Number of positive steps}}{n - 1}
\]

If this ratio exceeds a threshold (e.g., 0.6), we consider the sequence to exhibit an **upward trend**.

### Python Implementation

```python
def first_order_difference(arr: list) -> bool:
    positive_steps = sum(1 for i in range(len(arr) - 1) if arr[i+1] > arr[i])
    return positive_steps / (len(arr) - 1) >= 0.6

