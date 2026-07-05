# Stepper-Motor-Hand-Controller-
AI Stepper Motor Hand Controller
This project allows you to control the speed of a stepper motor using real-time AI hand tracking via your webcam. It calculates the distance between your right thumb and index finger and maps that distance to the motor's speed.
Hardware Requirements
•	Arduino Uno
•	28BYJ-48 Stepper Motor
•	ULN2003 Motor Driver Board
•	Jumper Wires
•	Webcam
Arduino Wiring Connections
Connect the ULN2003 motor driver board to the Arduino Uno as follows:
•	IN1: Arduino Digital Pin 8
•	IN2: Arduino Digital Pin 9
•	IN3: Arduino Digital Pin 10
•	IN4: Arduino Digital Pin 11
•	VCC / +: Arduino 5V
•	GND / -: Arduino GND
Note: The AccelStepper library requires the specific pin sequence of 8, 10, 9, 11 for this specific motor to spin correctly.
Software Setup
1. Arduino Preparation
	1.	Open the Arduino IDE.
	2.	Open the Library Manager and install the AccelStepper library.
	3.	Select your Arduino's port and upload the provided C++ code.
	4.	Completely close the Serial Monitor (Python cannot connect if the Serial Monitor is open).
2. Python Preparation
	1.	Open your terminal or command prompt.
	2.	Install the required dependencies by running: pip install opencv-python pyserial mediapipe ultralytics
	3.	Open Skeleton.py in your code editor (like PyCharm).
	4.	Update the SERIAL_PORT variable at the top of the script to match your specific Arduino port (e.g., SERIAL_PORT = '/dev/cu.usbserial-120').
Usage Instructions
	1.	Ensure your Arduino is plugged into your computer via USB.
	2.	Run the Skeleton.py script.
	3.	Wait a moment for the AI models to load and the camera window to appear.
	4.	Raise your right hand into the camera frame.
	5.	Pinch your thumb and index finger together to stop the motor (Speed: 0).
	6.	Stretch your thumb and index finger wide apart to accelerate the motor (Speed: 2000 max).
	7.	Press the q key on your keyboard while the camera window is active to safely quit the program and stop the motor.
