AI Stepper Motor Controller
This project uses computer vision to control a stepper motor's speed and an LED's brightness based on hand gestures. It uses MediaPipe for hand tracking and YOLO for object detection.
Hardware Pin Connections
Ensure your components are connected to the following pins on your Arduino:
Component	Arduino Pin
Stepper IN1	8
Stepper IN2	10
Stepper IN3	9
Stepper IN4	11
LED (+) (PWM)	3
LED (-)	GND
Requirements
•	Python Version: 3.11
•	Required Libraries: opencv-python, pyserial, mediapipe, ultralytics
Setup Instructions
	1.	Install Dependencies: Install the required packages specifically for your Python 3.11 environment by running this command in your terminal:
python3.11 -m pip install opencv-python pyserial mediapipe ultralytics

	2.	Arduino Configuration:
•	Upload the Arduino sketch to your board.
•	Ensure the LED is connected to Pin 3 (as Pin 9 is currently occupied by the stepper motor).
	3.	Run the Controller:
•	Open Skeleton.py and ensure SERIAL_PORT is set to your active port (e.g., /dev/cu.usbserial-120).
•	Execute the script using Python 3.11:
python3.11 /Users/eretuka/antigravity/Stepper-Motor-Hand-Controller-/Skeleton.py

	4.	Usage:
•	Pinch your thumb and index finger in front of the camera to control motor speed and LED brightness.
•	Press 'q' to quit the application.
