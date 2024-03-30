import cv2
import math
from ultralytics import YOLO

model = YOLO('yolov8n-pose.pt')
vid = cv2.VideoCapture(0) 

while vid.isOpened():
    success, frame = vid.read()

    results = model(frame)

    for info in results:
        parameters = info.boxes
        for box in parameters:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            confidence = box.conf[0]
            conf = math.ceil(confidence * 100)

            height = y2 - y1
            width = x2 - x1
            threshold = height - width

            if conf > 80:
                cv2.rectangle(frame, (x1,y1), (x1+x2, y1+y2), (0,255,0), 2)
            if threshold < 0:
                cv2.rectangle(frame, (x1,y1), (x1+x2, y1+y2), (0,0,255), 2)

            else: pass
    
    # results = model.predict(source=0, show=True, conf=0.5, imgsz=320,save=True)

    # annotated_frame = results[0].plot()

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # else:
    #     break

vid.release()
cv2.destroyAllWindows()

