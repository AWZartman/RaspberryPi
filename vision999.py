import json
import requests
import base64
import time
from time import sleep
import picamera
import RPi.GPIO as GPIO
import sys

# Setting the api key and GPIO pins 
google_api=sys.argv[1]
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use GPIO numbering

sleepAttentionTime = 2  #Give the user enough time to read the screen then look down at the leds
sleepLowTime = .5       #Amount of time to have the LED Off in the loop
sleepHighTime = 1       #Amount of time to have the LED On in the loop

ledPin1=4
GPIO.setup(ledPin1, GPIO.OUT, initial=GPIO.LOW)
ledPin2=5
GPIO.setup(ledPin2, GPIO.OUT, initial=GPIO.LOW)
ledPin3=6
GPIO.setup(ledPin3, GPIO.OUT, initial=GPIO.LOW) 
int_blink = 0;

# Capturing the image for Google Vision.
with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.start_preview(fullscreen=False,window=(100,200,300,300))
    camera.framerate = 15
    camera.start_recording('video.h264', resize=(320, 240))
    camera.wait_recording(5)
    camera.capture('dd.jpg', use_video_port=True)
    camera.wait_recording(5)
    camera.stop_recording()

# Creating Request to send to Google Vision 
    with open('dd.jpg', 'rb') as image: 
     try:
       image_content = base64.b64encode(image.read())
       req_file = image_content.decode('UTF-8')
       url = 'https://vision.googleapis.com/v1/images:annotate?key=%s'%google_api
       data = {
       'requests':[
           {
             'image':{
               'content': req_file
             },
             'features':[
               {
                'type':'TEXT_DETECTION',
                'maxResults':1
               }
             ]
           }
         ]
       }

# Sending Request to Google Vision to identify the number
       response = requests.post(url, data=json.dumps(data))
       print(response) 
       json_data = response.json()
       s = json_data['responses'][0]['textAnnotations'][0]['description']
       int_blink = int(s)
       print 'The number is >> ', int_blink
       print '!!!!!!!! WATCH THE LED BLINK ', int_blink , ' TIMES !!!!!!!!'  
     except:
       print("The number was not identified") 
       print("!!!!!!!! PLEASE TRY AGAIN !!!!!!!!") 
    camera.stop_preview()
    camera.close() 


hundreds = divmod(int_blink,100)
blinkHundreds = hundreds[0]
#print 'blinkHundreds = ', blinkHundreds

tens= divmod(hundreds[1], 10)
blinkTens = tens[0]
#print 'blinkTens = ', blinkTens

blinkOnes = tens[1]
#print 'blinkOnes = ', blinkOnes

print 'Blinking the Hundreds ', blinkHundreds, 'times'
if blinkHundreds > 0:
 
  # Wait 1 second before starting the LED Blink loop
  sleep(1.5)

  # Blinks the LED as per the integer identified 
  for x in range(0,blinkHundreds):
     GPIO.output(ledPin3, GPIO.HIGH)
     sleep(.5) # Sleep for 1 second
     GPIO.output(ledPin3, GPIO.LOW)
     sleep(.5) # Sleep for 1 second


print ' Blinking the Tens ', blinkTens, 'times'
if blinkTens > 0:
  # Wait 1 second before starting the LED Blink loop
  sleep(1.5)

  # Blinks the LED as per the integer identified 
  for x in range(0,blinkTens):
     GPIO.output(ledPin2, GPIO.HIGH)
     sleep(.5) # Sleep for 1 second
     GPIO.output(ledPin2, GPIO.LOW)
     sleep(.5) # Sleep for 1 second



print '  Blinking the Ones ', blinkOnes, 'times'
if blinkOnes > 0:
    # Wait 1 second before starting the LED Blink loop
  sleep(1.5)

  # Blinks the LED as per the integer identified 
  for x in range(0,blinkOnes):
     GPIO.output(ledPin1, GPIO.HIGH)
     sleep(.5) # Sleep for 1 second
     GPIO.output(ledPin1, GPIO.LOW)
     sleep(.5) # Sleep for 1 second
