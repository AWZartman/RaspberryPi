# RaspberryPi Vision999

Vision999 uses an attached camera to take a picture of a number 1-999.  The picture is then send up to Google vision for processing (an account is needed to get a token to be passsed into the program)

If the number is recognized, the LED's blink to match the number starting with the "Hundreds" LED, then the "Tens" LED and then the Ones" LED position.

For this project, I am using the Sparkfun Pi Wedge (Adafruit calls it a T-Cobbler) to make it easier for students to see and connect connectors and to save on wear and tear on the Raspberry Pi GPIO pins.

Also, I wanted to be able to setup multiple projects, each on their own breadboard and simply transfer the Pi Wedge from board to board to demonstrate many projects in a short amount of time with only one Raspberry Pi available.

## Wiring Diagram with Sparkfun Pi Wedge

![Fritzing Wiring diagram for Vision999 project](/images/Vision999_wiring_diagram.png "Vision999 wiring diagram")

When using a Pi Wedge/T-Cobbler, you need to make sure that you use Broadcom GPIO numbering (BCM) instead of board numbering

_GPIO.setmode(GPIO.BCM)_

As you can see, this is still a simple project using only 4 wires, 3 resisters and 3 LEDs.
