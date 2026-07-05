import cv2
import math
import serial
import mediapipe as mp
from ultralytics import YOLO

# --- ARDUINO CONNECTION ---
# Update this string to match your exact Arduino port!
SERIAL_PORT = '/dev/cu.usbserial-120'

try:
    arduino = serial.Serial(SERIAL_PORT, 115200, timeout=0.01)
    print("Arduino connected successfully!")
except Exception as e:
    print(f"Arduino not found: {e}")
    arduino = None


# --- HELPER FUNCTIONS ---

def count_left_fingers(landmarks):
    """Rotation-proof finger counting using 3D distance from the wrist/palm"""
    count = 0

    def get_dist(p1, p2):
        return math.hypot(landmarks.landmark[p1].x - landmarks.landmark[p2].x,
                          landmarks.landmark[p1].y - landmarks.landmark[p2].y)

    # 1. Thumb Logic: Check if Thumb Tip (4) is further from Pinky Base (17) than the Thumb Joint (3) is.
    if get_dist(4, 17) > get_dist(3, 17):
        count += 1

    # 2. Other Fingers Logic: Check if Tip is further from the Wrist (0) than the PIP joint is.
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    for tip, pip in zip(tips, pips):
        if get_dist(tip, 0) > get_dist(pip, 0):
            count += 1

    return count


def draw_pinch_beam_and_get_dist(frame, landmarks, width, height, color=(0, 255, 255)):
    """Draws a beam between thumb and index and returns distance in pixels"""
    thumb = landmarks.landmark[4]
    index = landmarks.landmark[8]

    x1, y1 = int(thumb.x * width), int(thumb.y * height)
    x2, y2 = int(index.x * width), int(index.y * height)

    cv2.line(frame, (x1, y1), (x2, y2), color, 3)
    cv2.circle(frame, (x1, y1), 5, color, cv2.FILLED)
    cv2.circle(frame, (x2, y2), 5, color, cv2.FILLED)

    return int(math.hypot(x2 - x1, y2 - y1))


# --- INITIALIZATION ---
model = YOLO('yolov8n.pt')
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

holistic = mp_holistic.Holistic(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Remember to change to 0 if your built-in webcam acts up!
cap = cv2.VideoCapture(1)

print("Starting camera... Press 'q' to quit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    h, w, _ = frame.shape

    # Default states to send to Arduino
    right_speed = 0
    left_finger_count = 0

    # YOLO Detection (Objects & People)
    results = model(frame, stream=True, verbose=False)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 105, 180), 2)

    # MediaPipe Tracking (Body & Hands)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    holistic_results = holistic.process(rgb_frame)

    # LEFT HAND (Controls Synthesizer Buzzer)
    if holistic_results.left_hand_landmarks:
        mp_drawing.draw_landmarks(frame, holistic_results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        left_finger_count = count_left_fingers(holistic_results.left_hand_landmarks)

    # RIGHT HAND (Controls Stepper Motor Speed)
    if holistic_results.right_hand_landmarks:
        mp_drawing.draw_landmarks(frame, holistic_results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        right_dist = draw_pinch_beam_and_get_dist(frame, holistic_results.right_hand_landmarks, w, h, (0, 255, 255))

        # Calibrated Logic: Distance 25 to 600 maps to Speed 0 to 2000
        if right_dist < 25:
            right_speed = 0
        else:
            mapped_speed = int((right_dist - 25) * 3.5)
            right_speed = min(mapped_speed, 2000)  # Cap at 2000

    # SEND DATA TO ARDUINO
    if arduino:
        # Format: "Speed,FingerCount\n"
        data_string = f"{right_speed},{left_finger_count}\n"
        arduino.write(data_string.encode())

    # HUD (Heads Up Display)
    cv2.putText(frame, f'Motor Speed: {right_speed}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f'Left Fingers (Pitch): {left_finger_count}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (255, 255, 255), 2)

    cv2.imshow('AI Hardware Controller (Musical Edition)', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
if arduino:
    arduino.write(b"0,0\n")
    arduino.close()
cap.release()
cv2.destroyAllWindows()
holistic.close()