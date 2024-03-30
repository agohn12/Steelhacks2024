# SteelHacks Project 2024: One Call Away
### Team: Austin, Ly, and Morgan
The goal of One Call Away, is to detect a fall, assess its severity, and autonomously call the victim's emergency contact if the victim remains fallen for more than thirty seconds. Note that in our demo, this time period is shortened to three seconds for practical purposes.

We are a group of three newbies trying to make a very complex program... what could go wrong?

## Introduction

1 in every 4 Americans that are over the age of 65 fall every year. That's a lot! Many of these falls result in severe complications and even death. When elderly people fall they are often unable to get up and need assistance. 

805,000 Americans every year also suffer from heart attacks, 3.4 million Americans suffere from seizures, and 2.8 million Americans also suffer from Anemia. These complications often lead to sudden collapsing. When people fall they often need assistance even if no one is around.

## Code description

All of the code for this project can be run in one file, OneCallAway.py. We imported the following libraries & APIs:
* OpenCV, for doing tasks based on computer vision
* Ultralytics YOLOv8, a real-time object detection model
* Twilio, an API that makes phone calls with custom messages
* Pygame, for playing a pre-recorded audio message

In the Supplementary Files folder, you will find WIPs and additional materials that could be incorporated into OneCallAway.py to make object detection more robust. For example, classes.txt is an array of different objects. This could be used to distinguish people from inanimate objects. 

## How to run

After cloning the repository run the command, "Python3 OneCallAway.py". Once you run this command the program will begin shortly. A screen will pop displaying the webcam output:

<img width="1173" alt="Screenshot 2024-03-30 at 4 03 10 PM" src="https://github.com/agohn12/Steelhacks2024/assets/114429170/1a3e0e84-eeb9-4002-a875-45428902080c">

When a person walks into the frame, a green rectangle will surrond the person indicating the person has been detected by the camera:

<img width="1172" alt="Screenshot 2024-03-30 at 4 05 01 PM" src="https://github.com/agohn12/Steelhacks2024/assets/114429170/5b249df2-4a28-4e86-b718-14458aa2f9de">

If a camera believes a person falls, a redbox will appear around the person indicating that a fallen person has been detected. A message will also appear that the program will be calling emergency contacts in 3 seconds (3 seconds for demo reasons, would normally be 30 seconds). 

<img width="1170" alt="Screenshot 2024-03-30 at 4 09 53 PM" src="https://github.com/agohn12/Steelhacks2024/assets/114429170/5d2de05b-e8ba-431c-908e-2155f43b965d">

If a person gets up off the floor before the call happens. The green box will return and the call will be cancelled. If the person is detected to be fallen for more than 3 seconds, an audio file will play notifying the person who fell that emergency contacts have been notified.

The phone call to emergency contacts will play a customized message that alerts the contact that someone they know as fallen and emergency services are on the way.


