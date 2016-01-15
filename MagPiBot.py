# Import libary functions we need
import RPi.GPIO as GPIO
import time
import sys
GPIO.setmode(GPIO.BCM)
# Set which GPIO pins the drive outputs are connected to
DRIVE_1 = 4
DRIVE_2 = 18
# Set the GPIO pins of the ultrasonic sensor
TRIG = 40
ECHO = 37
# Set the GPIO pins of the line sensor
CENTRE = 31
LEFT = 32
RIGHT = 33
# Set all of the drive pins as output pins
GPIO.setup(DRIVE_1, GPIO.OUT)
GPIO.setup(DRIVE_2, GPIO.OUT)
# Function to set both drives off
def RobotStop():
 GPIO.output(DRIVE_1, GPIO.LOW)
 GPIO.output(DRIVE_2, GPIO.LOW)
# Function to set both drives on
def RobotForward():
 GPIO.output(DRIVE_1, GPIO.HIGH)
 GPIO.output(DRIVE_2, GPIO.HIGH)
# Set ultrasonic pins function
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
# Give sensor time to settle
GPIO.output(TRIG, False)
print “Waiting for ultrasonic sensor to settle...”
time.sleep(2)
print “Settled!”
# Set line follower pins as inputs
GPIO.setup(CENTRE, GPIO.IN)
GPIO.setup(LEFT, GPIO.IN)
GPIO.setup(RIGHT, GPIO.IN)
try:
 # Start by turning all drives off
 RobotStop()
 raw_input(“We’re ready to roll, press ENTER to continue”)
 while True:
 # Get distance to object
 GPIO.output(TRIG, True)
 time.sleep(0.00001)
 GPIO.output(TRIG, False)
 while GPIO.input(ECHO)==0:
 pulse_start = time.time()
 while GPIO.input(ECHO)==1:
 pulse_end = time.time()
 pulse_duration = pulse_end - pulse_start
 distance = pulse_duration * 17150
 distance = round(distance, 2)
 # Check line followers
 line_left = GPIO.input(LEFT)
 line_right = GPIO.input(RIGHT)
 if distance > 5:
 if line_left == 0:
 # Drive 1 state
 GPIO.output(DRIVE_1, GPIO.HIGH)
 # Drive 2 state
 GPIO.output(DRIVE_2, GPIO.LOW)
 # Get back on course
 time.sleep(1)
 RobotForward()
 time.sleep(0.5)
 elif line_right == 0:
 # Drive 1 state
 GPIO.output(DRIVE_1, GPIO.LOW)
 # Drive 2 state
 GPIO.output(DRIVE_2, GPIO.HIGH)
 # Get back on course
 time.sleep(1)
 RobotForward()
 time.sleep(0.5)
 else:
 # Move forward
 RobotForward()
 else:
 RobotStop()
 print ‘I have stopped, please turn off my power!’
 GPIO.cleanup()
 sys.exit()

except KeyboardInterrupt:

 # CTRL+C exit, turn off the drives and release GPIO pins
 print ‘Stopped early, please turn off my power!’
 RobotStop()
 GPIO.cleanup()
