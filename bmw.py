import RPi.GPIO as GPIO # always needed with RPi.GPIO  
import time
import curses

from os import system as sys
from picamera import PiCamera

camera = PiCamera()
captura=1

# get the curses screen window
screen = curses.initscr()
# turn off input echoing
curses.noecho()
# respond to keys immediately (don't wait for enter)
curses.cbreak()
 
# map arrow keys to special values
screen.keypad(True)
  
GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM  

#################################################################
#			Variables		  		#
#################################################################

#For Motor #1
GPIO.setup(18, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
  
p24 = GPIO.PWM(24, 100)
p23 = GPIO.PWM(23, 100)
p18 = GPIO.PWM(18, 100)    

#For Motor #2
GPIO.setup(13, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)

p27 = GPIO.PWM(27, 100)
p17 = GPIO.PWM(17, 100)
p13 = GPIO.PWM(13, 100)

#avari
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

LastKey = ""
#################################################################
#			Functions		  		#
#################################################################

def Stop():
            p18.start(0)
            p23.start(0)
            p24.start(0)

            p13.start(0)
            p27.start(0)
            p17.start(0)        

def Left():  
            p23.start(0)
            p24.start(100)

            p27.start(0)
            p17.start(100)

            p18.start(100)
            p13.start(30)

def Right():
            p23.start(100)
            p24.start(0)
            
            p27.start(100)
            p17.start(0)
            
            p13.start(100)
            p18.start(30)
            
def Down():
            p23.start(100)
            p24.start(0)
            
            p27.start(0)
            p17.start(100)

            
            p13.start(100)
            p18.start(100)

            forward=0
            backward=100   

def Up():
            p23.start(0)
            p24.start(100)

            p27.start(100)
            p17.start(0)

            
            p13.start(100)
            p18.start(100)

            forward=100
            backward=0

try:
    while True:
        char = screen.getch()
        if char == ord('q'):
            break
        elif char == ord('p'):
            LastKey='p'
            time.sleep(0.5)
            camera.capture('/home/pi/Documents/lucru/YoloV2NCS/data/image_captura_%s.jpg' %captura)
            print ('Captura completa!%s imagini captate\n' %captura)
            sys("cd YoloV2NCS && python3 ./detectionExample/Main.py --image ./data/image_captura_%s.jpg" % captura)
            captura+=1
        elif char == ord(' '):
            LastKey=' '
            Stop()
            GPIO.output(20,True)
            GPIO.output(21,True)

            time.sleep(0.5)

            GPIO.output(20,False)
            GPIO.output(21,False)

            time.sleep(0.5)

        elif char == curses.KEY_RIGHT:
            Right() 
           
        elif char == curses.KEY_LEFT:
            Left()

        elif char == curses.KEY_UP:
            Up()

        elif char == curses.KEY_DOWN:
            Down()
        else:
            print ('Nothing Entred!\n')

finally:
    # shut down cleanly 
    print ('In the finally section now')
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    p13.stop()               
    p17.stop()
    p27.stop()

    p23.stop()               
    p24.stop()
    p18.stop()

    GPIO.cleanup()          

p13.stop()                 
p17.stop()
p27.stop()
  
p23.stop()               
p24.stop()
p18.stop()

GPIO.cleanup()
