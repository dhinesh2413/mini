from ultralytics import YOLO
#print(YOLO("yolov8n.pt"))
import cv2

model=YOLO(r"C:\GENAI\runs\detect\train2\weights\best.pt")

cap=cv2.VideoCapture("traffic.mp4")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    results=model(frame)

    for result in results:
        for box in result.boxes:
            x1,y1,x2,y2=map(int,box.xyxy[0])
            confidence=box.conf[0].item()
            cls=int(box.cls[0])

            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            label=f"{model.names[cls]}{confidence:.2f}"
            cv2.putText(frame,label,(x1,y1-10),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,0),2)

    cv2.imshow("YOLOv8 Detection",frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

