import cv2
import math
import time
from ultralytics import YOLO

model = YOLO('yolov8n-pose.pt')
vid = cv2.VideoCapture(0) 

classnames = []
with open('SteelHacks2024/classes.txt', 'r') as f:
    classnames = f.read().splitlines()

starting_time = time.time()
begin = starting_time
falling = False
hold = 0

while vid.isOpened():
    success, frame = vid.read()

    results = model(frame)

    for info in results:
        parameters = info.boxes
        for box in parameters:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            confidence = box.conf[0]
            class_detect = box.cls[0]
            class_detect = int(class_detect)
            class_detect = classnames[class_detect]
            conf = math.ceil(confidence * 100)

            height = y2 - y1
            width = x2 - x1
            threshold = height - width

            font = cv2.FONT_HERSHEY_SIMPLEX

            if falling:
                curr_elapsed = time.time() - starting_time
                hold = hold + curr_elapsed
                print(hold)
                if hold > 5:
                    print("FALL")
                    vid.release()
                    cv2.destroyAllWindows()
                    # print("Elapsed: {}".format(curr_elapsed))
            else:
                hold = 0

            if conf > 80:
                falling = False
                cv2.rectangle(frame, (x1,y1), (x1+x2, y1+y2), (0,255,0), 2)
                # elapsed_time = time.time() - starting_time
                # print("Elapsed: {}".format(elapsed_time))
            if threshold < 0 and class_detect == 'person' and y1 > 325:
                starting_time = time.time()
                falling = True
                cv2.rectangle(frame, (x1,y1), (x1+x2, y1+y2), (0,0,255), 2)
                cv2.putText(frame,  
                'Fall Detected: calling in 3s',  
                (50, 50),  
                font, 1,  
                (0, 255, 255),  
                2,  
                cv2.LINE_4) 
                # elapsed_time = time.time() - starting_time

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

