# import the opencv library 
import cv2
from ultralytics import yolo

face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_upperbody.xml")


# define a video capture object 
vid = cv2.VideoCapture(0) 
  
while(True): 
      
    # Capture the video frame 
    # by frame 
    ret, frame = vid.read() 

    if ret == True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        coordinate_list = face.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3) 
        body_list = body.detectMultiScale(gray, 1.1, 2)

        # drawing rectangle in frame
        for (x,y,w,h) in coordinate_list:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            print(y)
    # Display the resulting frame 
    cv2.imshow('frame', frame) 
      
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 