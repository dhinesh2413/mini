import cv2
import numpy as np
from ultralytics import YOLO

# Load trained YOLO model
model = YOLO(r"C:\GENAI\runs\detect\train2\weights\best.pt")  # Replace with your trained model

# Open video file or webcam
cap = cv2.VideoCapture("traffic.mp4")

# Camera calibration values (adjust these)
FOCAL_LENGTH = 600  # Focal length of the camera in pixels
KNOWN_WIDTH = 180  # Approximate real-world width of a car in cm

def calculate_distance(pixel_width):
    """Calculate real-world distance from camera using pixel width"""
    if pixel_width > 0:
        return (KNOWN_WIDTH * FOCAL_LENGTH) / pixel_width
    return None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # End of video

    results = model(frame)  # Run YOLO detection
    vehicle_positions = []  # Store vehicle positions

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0]  # Get bounding box
            pixel_width = x2 - x1  # Width of detected vehicle in pixels
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2  # Find vehicle center

            distance = calculate_distance(pixel_width)  # Compute distance

            if distance:
                vehicle_positions.append((center_x, center_y, distance))

                # Display distance on video frame
                cv2.putText(frame, f"{distance:.2f} cm",
                            (int(x1), int(y1) - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            0.6, (0, 255, 0), 2)
    
    # Compute distances between each vehicle
    for i in range(len(vehicle_positions)):
        for j in range(i + 1, len(vehicle_positions)):
            x1, y1, d1 = vehicle_positions[i]
            x2, y2, d2 = vehicle_positions[j]

            # Calculate Euclidean distance in pixels
            pixel_distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

            # Convert pixel distance to real-world distance
            real_distance = abs(d1 - d2)  # Approximate relative distance

            # Draw line between vehicles
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
            mid_x, mid_y = int((x1 + x2) / 2), int((y1 + y2) / 2)
            
            # Display distance between vehicles
            cv2.putText(frame, f"{real_distance:.2f} cm",
                        (mid_x, mid_y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.6, (0, 0, 255), 2)

    # Show video
    cv2.imshow("Vehicle Distance Estimation", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
