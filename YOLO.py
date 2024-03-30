#Use twilio to access a phone number and manage phone calls
from twilio.rest import Client
import cv2
import math
import time
from ultralytics import YOLO

#Main function
def main():
    fall_detected = False
    i = 0
    #Continues to check if a fall was detected
    while (not fall_detected):

        model = YOLO('yolov8n-pose.pt')
        vid = cv2.VideoCapture(0)
        vid.set(3, 1600)
        vid.set(4, 1600)

        # classnames = []
        # with open('SteelHacks2024/classes.txt', 'r') as f:
        #     classnames = f.read().splitlines()

        starting_time = time.time()
        begin = starting_time
        falling = False
        hold = 0
        screen_width = 0
        screen_height = 0


        # if vid.isOpened(): 
        #     # get vcap property 
        #     screen_width  = vid.get(3)  # float `width`
        #    screen_height = vid.get(4)  # float `height`

        #     fps = vid.get(5)

        while vid.isOpened():
            success, frame = vid.read()

            results = model(frame)

            for info in results:
                parameters = info.boxes
                for box in parameters:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    confidence = box.conf[0]
                    # class_detect = box.cls[0]
                    # class_detect = int(class_detect)
                    # class_detect = classnames[class_detect]
                    conf = math.ceil(confidence * 100)

                    height = y2 - y1
                    width = x2 - x1
                    threshold = height - width

                    font = cv2.FONT_HERSHEY_SIMPLEX

                    if falling:
                        curr_elapsed = time.time() - starting_time
                        hold = hold + curr_elapsed
                        print(hold)
                        if hold > 3:
                            print("HELP CALLED")
                            fall_detected = True
                            make_call()
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
                    if threshold < 0 and y1 > 450:
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
                    else:
                        falling = False
                        # elapsed_time = time.time() - starting_time

                    # else: pass
            
            # results = model.predict(source=0, show=True, conf=0.5, imgsz=320,save=True)

            # annotated_frame = results[0].plot()

            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # else:
            #     break

        vid.release()
        cv2.destroyAllWindows()
    
    #If fall detected make a call to emergency contacts
    if (fall_detected):
         make_call()

#Checks if fall has been detected
def check_fall(i):
        if (i == 3):
            return True
        return False

#Makes a call to emergency contacts through twilio
def make_call():

    # Twilio phone number, phone number that is placing the call
    TWILIO_PHONE_NUMBER = "+18557111432"

    # Emergency phone number to dial
    DIAL_NUMBERS = ["+17177817088"]

    # URL that contains instructions for phone call
    TWIML_INSTRUCTIONS_URL = "https://handler.twilio.com/twiml/EH9b2bab7c221a0a5d0ea9429c7373aa48"

    #Client arguments include SID and Auth token for account
    client = Client("AC6c2178769eeecececdc042eaa9e695a8", "3def8d936d075d8cd71bea2e6d3ed581")


    def dial_numbers(numbers_list):
        
        #Dials numbers in numbers list
        for number in numbers_list:
            print("Dialing " + number)

            client.calls.create(to=number, from_=TWILIO_PHONE_NUMBER, url=TWIML_INSTRUCTIONS_URL, method="GET")

    if __name__ == "__main__":
        dial_numbers(DIAL_NUMBERS)

if __name__ == "__main__":
    main()