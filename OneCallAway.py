import cv2
import math
import time
#Computer vision libraries
from ultralytics import YOLO
from twilio.rest import Client
import pygame

#Main function
def main():
    #Boolean to track if a fall has occured
    fall_detected = False

    # continues to check if fall was detected
    while (not fall_detected):
        #Checks if fall has been detected
        fall_detected = check_fall()

    #If fall has been detected make phone call to emergency contacts
    if(fall_detected):
        make_call()

#Function that moitors webcam and checks for people falling
def check_fall():
    
    #Loads an official model from YOLO library
    model = YOLO('yolov8n-pose.pt')
    #Starts webcam
    vid = cv2.VideoCapture(0)
    #Set the video frame dimensions
    vid.set(3, 1600)
    vid.set(4, 1600)

    # classnames = []
    # with open('SteelHacks2024/classes.txt', 'r') as f:
    #     classnames = f.read().splitlines()

    #Declare variables to track time of person on ground
    starting_time = time.time()
    begin = starting_time
    falling = False
    hold = 0

    #While webcam is streaming output
    while vid.isOpened():
        #Read in video output
        success, frame = vid.read()
        #Used to detect people
        results = model(frame)

        #For every person in the webcam frame
        for info in results:
            #Gets info of boxes
            parameters = info.boxes
            
            #Checks all boxes in frame
            for box in parameters:
                #Gets box properties
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

                #Sets font for screen
                font = cv2.FONT_HERSHEY_SIMPLEX

                #Dispays Name and Demo in corners
                cv2.putText(frame, 'One Call Away', (50, 50), font, 1,
                    (0, 255, 255), 2, cv2.LINE_4)
                
                cv2.putText(frame, 'Demo', (1100, 50), font, 1,
                    (0, 255, 255), 2, cv2.LINE_4)

                #If falling detected check time; otherwise set hold back to zero
                if falling:
                    #Gets time on the ground
                    curr_elapsed = time.time() - starting_time
                    hold = hold + curr_elapsed

                    #If time on ground is above 3 seconds
                    if hold > 3:
                        #Return true to call for help
                        print("HELP CALLED")
                        # Initialize pygame mixer
                        pygame.mixer.init()
                        # Load sound file that plays "Emergency contact notified"
                        sound_file = "audio.wav"
                        sound = pygame.mixer.Sound(sound_file)
                        # Play sound
                        sound.play()
                        # Wait for sound to finish
                        pygame.time.wait(int(sound.get_length() * 1000))
                        # Clean up: after message finishes, close video and make the call
                        vid.release()
                        cv2.destroyAllWindows()
                        return True
                else:
                    hold = 0

                #If confident that object is detected
                if conf > 80:
                    #reset falling in case it is initially true
                    falling = False
                    #Draws green rectangle around object
                    cv2.rectangle(frame, (x1,y1), (x1+x2, y1+y2), (0,255,0), 2)

                #If width > height (threshold, laying position) and top of box in bottom of frame
                if threshold < 0 and y1 > 450:
                    #Starts time of laying position
                    starting_time = time.time()
                    falling = True
                    #Draws red rectangle
                    cv2.rectangle(frame, (x1,y1), (x1+x2, y1+y2), (0,0,255), 2)
                    #Displays message on screen
                    cv2.putText(frame,  
                    'Fall Detected: calling in 3s',  
                    (50, 90),  
                    font, 1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_4)
                else:
                    falling = False

        #Displays video output on screen
        cv2.imshow('frame', frame)

        #If q key is put ends video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    #Exits program and ends vido processes
    vid.release()
    cv2.destroyAllWindows()

    #return False

#Function to make call to emergency contacts
def make_call():
    #Phone number to make call hosted by Twilio
    TWILIO_PHONE_NUMBER = "+18557111432"
    #Emergency numbers to dial
    DIAL_NUMBERS = ["+17177817088"]
    #Link to instructions for phone message on twilio. (Phone-Message-xml contains code that is on twilio)
    TWIML_INSTRUCTIONS_URL = "https://handler.twilio.com/twiml/EH9b2bab7c221a0a5d0ea9429c7373aa48"

    #Creates a client using twilio account ID and authentication token. 
    #Authentication token may not be public or twilio will revoke token. 
    #Therefore, Authentication token must be redacted and filled in when downloaded from github. 
    #Contact code author, if authentication token is needed.
    client = Client("AC6c2178769eeecececdc042eaa9e695a8", "***REDACTED***")

    #dials all numbers in emergency contact list
    def dial_numbers(numbers_list):
        for number in numbers_list:
            print("Dialing " + number)
            #Makes phone call for every emergency number
            client.calls.create(to=number, from_=TWILIO_PHONE_NUMBER, url=TWIML_INSTRUCTIONS_URL, method="GET")
    
    if __name__ == "__main__":
        dial_numbers(DIAL_NUMBERS)

if __name__ == "__main__":
    main()
