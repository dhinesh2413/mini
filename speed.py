import cv2
import numpy as np
from ultralytics import YOLO
import time

model = YOLO(r"C:\GENAI\runs\detect\train2\weights\best.pt")  # Load trained YOLO model
cap = cv2.VideoCapture("traffic.mp4")

previous_positions = {}  # Store last known positions and timestamps

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    start_time = time.time()  # Capture frame timestamp
    results = model(frame)

    current_positions = {}

    for r in results:
        for i, box in enumerate(r.boxes):
            x1, y1, x2, y2 = box.xyxy[0]  # Bounding box coordinates
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            current_positions[i] = (center_x, center_y, start_time)  # Store new position

            if i in previous_positions:
                prev_x, prev_y, prev_time = previous_positions[i]
                Δt = start_time - prev_time  # Time difference

                if Δt > 0:  # Prevent division by zero
                    pixel_distance = np.sqrt((center_x - prev_x) ** 2 + (center_y - prev_y) ** 2)
                    speed = pixel_distance / Δt  # Speed in px/sec

                    cv2.putText(frame, f"Speed: {speed:.2f} px/sec", 
                                (int(x1), int(y1) - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                0.6, (0, 255, 255), 2)

    previous_positions = current_positions  # Update previous positions
    cv2.imshow("Speed Estimation", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
