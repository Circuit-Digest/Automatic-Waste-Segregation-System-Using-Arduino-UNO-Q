# Automatic-Waste-Segregation-System-Using-Arduino-UNO-Q

# Automatic Waste Segregation System Using Arduino UNO Q
An intelligent, AI-powered waste sorting system that automatically identifies and segregates waste into different categories using Computer Vision and Machine Learning. Built on the **Arduino UNO Q**, this project leverages its hybrid dual-brain architecture to handle complex AI processing and real-time hardware control simultaneously.

## 🚀 Overview

Proper waste sorting is critical for environmental sustainability. This project simplifies the process by using a USB camera and an Edge Impulse-trained model to detect four types of waste: **Paper, Plastic, Cardboard, and Battery**.

| Waste Type | Action Triggered | Category |
| :--- | :--- | :--- |
| **Paper** | Servo rotates to 0° | Biodegradable |
| **Cardboard** | Servo rotates to 0° | Biodegradable |
| **Plastic** | Servo rotates to 180° | Non-Biodegradable |
| **Battery** | Buzzer Alert (2s) | Hazardous |

## 🛠️ Components Required

| Component | Quantity | Purpose |
| :--- | :---: | :--- |
| **Arduino Uno Q** | 1 | Main controller (Hybrid AI + MCU) |
| **USB Camera** | 1 | Real-time object detection |
| **USB Hub** | 1 | Connectivity for peripherals |
| **Micro Servo Motor** | 1 | Physical waste sorting mechanism |
| **Buzzer** | 1 | Hazardous item alert |
| **Jumper Wires** | - | Circuit connections |
| **Cardboard** | - | Bin structure fabrication |

## 🏗️ System Architecture

The system utilizes the **Arduino UNO Q**'s unique architecture:
1. **Python Layer (Linux Side):** Processes the video stream from the USB camera, runs the Edge Impulse object detection model, and handles the logic (stability checks, confidence thresholds, and cooldowns).
2. **Arduino Layer (MCU Side):** Receives commands from the Python layer via the **Router Bridge** and executes physical movements (Servo) or alerts (Buzzer).

## 💻 Software Used

- **[Edge Impulse](https://www.edgeimpulse.com/):** For data collection, model training, and generating the object detection dataset.
- **[Arduino App Lab](https://applab.arduino.cc/):** To develop the Python application and deploy the model.
- **Arduino IDE:** To program the hardware control logic onto the MCU side.

## 🔌 Circuit Diagram

- **Buzzer:** Connected to Pin **8**.
- **Servo Motor:** Connected to Pin **9**.
- **Camera:** Connected via USB Hub to the Arduino Uno Q.

## 📜 How It Works

1. **Detection:** The Python script captures frames from the USB camera.
2. **Analysis:** The `VideoObjectDetection` module analyzes frames with a confidence threshold of **0.82** (0.88 for Batteries).
3. **Stability Check:** To avoid false triggers, the system uses a **stability counter**. An action is only triggered if an object is detected consistently for **4 frames**.
4. **Action:**
   - **Biodegradable (Paper/Cardboard):** Servo moves to 0°, stays for 5 seconds, then returns to 90°.
   - **Non-Biodegradable (Plastic):** Servo moves to 180°, stays for 5 seconds, then returns to 90°.
   - **Hazardous (Battery):** Buzzer sounds for 2 seconds.

## 🛠️ Troubleshooting

- **Camera Issues:** Ensure adequate lighting. If detection is unstable, retrain the model with a more diverse dataset.
- **Servo Issues:** Check wiring and ensure the servo is receiving sufficient power.
- **Model Errors:** Verify all required libraries are installed in the Arduino App Lab environment.

## 🌟 Future Enhancements

- **Multi-Class Expansion:** Adding Glass, Metal, and Organic waste.
- **Mobile Integration:** App notifications for bin fill levels.
- **Solar Support:** Making the system off-grid for public use.
- **Cloud Analytics:** Tracking recycling rates via a web dashboard.

## 📄 License

This project is open-source. Feel free to use and modify it for your own educational and environmental projects!

---
*Developed by the Circuit Digest Team.*
