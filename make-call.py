#Used twilio to access a phone number and manage phone calls
from twilio.rest import Client

# Twilio phone number, phone number that is placing the call
TWILIO_PHONE_NUMBER = "+18557111432"

# Phone number to dial
DIAL_NUMBERS = ["+17177817088"]

# URL that contains instructions for phone call
TWIML_INSTRUCTIONS_URL = "https://handler.twilio.com/twiml/EH9b2bab7c221a0a5d0ea9429c7373aa48"

#Client arguments include SID and Auth token for account
client = Client("AC6c2178769eeecececdc042eaa9e695a8", "1db091b35c9adfd02741c8a2d8fa8e1a")


def dial_numbers(numbers_list):
    
    #Dials numbers in numbers list
    for number in numbers_list:
        print("Dialing " + number)

        client.calls.create(to=number, from_=TWILIO_PHONE_NUMBER, url=TWIML_INSTRUCTIONS_URL, method="GET")

if __name__ == "__main__":
    dial_numbers(DIAL_NUMBERS)