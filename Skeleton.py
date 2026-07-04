import cv2
import mediapipe as mp

# 1. Initialize MediaPipe Pose and Drawing modules
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    static_image_mode=False,  # False means optimize for continuous video tracking
    model_complexity=1,  # 1 is the sweet spot for real-time speed on a Mac
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# 2. Open live webcam (0 is your built-in Mac camera)
cap = cv2.VideoCapture(1)

print("Opening webcam... stand back so it can see your full body! Press 'q' to quit.")

while True:
    success, frame = cap.read()
    if not success:
        print("Error: Could not read from webcam.")
        break

    # Flip the image horizontally for a natural "mirror" effect
    frame = cv2.flip(frame, 1)

    # Convert the BGR frame to RGB for MediaPipe
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to find the body skeleton
    results = pose.process(imgRGB)

    # If a body is detected, draw the full wireframe skeleton automatically
    if results.pose_landmarks:
        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_draw.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),  # Red joint dots
            mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)  # Green connection lines
        )

    # Show the live feed window
    cv2.imshow("Live Skeleton Tracker", frame)

    # Wait 1 millisecond between frames, close window if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up resources when closing
cap.release()
cv2.destroyAllWindows()