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
sleepHighTime = .5       #Amount of time to have the LED On in the loop

ledPin1=4
ledPin2=5
ledPin3=6

GPIO.setup(ledPin1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ledPin2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ledPin3, GPIO.OUT, initial=GPIO.LOW) 

programAbort = 0
int_blink = 0;  # initialize the blink count to 0

# Capturing the image for Google Vision.
with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.start_preview(fullscreen=False,window=(100,200,500,500))
    camera.awb_mode = 'fluorescent'
    camera.image_effect = 'none'
    sleep(5)
    camera.capture('dd.jpg', use_video_port=True)
    camera.stop_preview()

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
       print '!!!!!!!! WATCH THE LED BLINK !!!!!!!!'  
     except:
       print("The number was not identified") 
       print("!!!!!!!! PLEASE TRY AGAIN !!!!!!!!")
       programAbort = 1   #If the number was not recognized, no need to continue
    camera.stop_preview()
    camera.close() 

if programAbort == 0:   #Test if we should continue

  hundreds = divmod(int_blink,100)
  blinkHundreds = hundreds[0]
  #print 'blinkHundreds = ', blinkHundreds

  tens= divmod(hundreds[1], 10)
  blinkTens = tens[0]
  #print 'blinkTens = ', blinkTens

  blinkOnes = tens[1]
  #print 'blinkOnes = ', blinkOnes

  def blink( pin, blinkCount ):
    # Blinks the LED defined by the pin blinkcount times 
    for x in range(0,blinkCount):
      GPIO.output(pin, GPIO.HIGH)
      sleep(sleepHighTime) # Sleep for 1 second
      GPIO.output(pin, GPIO.LOW)
      sleep(sleepLowTime) # Sleep for 1 second

  print 'Blinking the Hundreds ', blinkHundreds, 'times'
  if blinkHundreds > 0:
 
    # Wait before starting the LED Blink loop
    sleep(sleepAttentionTime)

    blink(ledPin3, blinkHundreds)


  print ' Blinking the Tens ', blinkTens, 'times'
  if blinkTens > 0:
    # Wait second before starting the LED Blink loop
    sleep(sleepAttentionTime)

    blink(ledPin2, blinkTens)


  print '  Blinking the Ones ', blinkOnes, 'times'
  if blinkOnes > 0:
    # Wait 1 second before starting the LED Blink loop
    sleep(sleepAttentionTime)

    blink(ledPin1, blinkOnes)
