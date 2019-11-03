import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GP = range(2,22)
GPIO.setup(GP, GPIO.OUT)


def lanetest():
    """turns on each GPIO from 1 to 20 individually for on e second"""
    GP = range(2,22)
    GS_off = [0]*len(GP)
    GS_on  = [1]*len(GP)
    m = -1
    n = len(GS_off)
    while True:
        m  += 1
        if m>=n:
            m=0
        print(m)
        GS = GS_off = [0]*len(GP)
        GS[m] = 1
        GPIO.output(GP,GS)
        time.sleep(1)
        #print "ALL on "
        #GPIO.output(GP,GS_on)
        #time.sleep(2)

def all_on():
    """Turns on all 20 GPIOs at once"""
    GP    = range(2,22)
    GS_on = [1]*len(GP)
    GPIO.output(GP,GS_on)
    print("all on")
    return 0

def all_off():
    """Turns off all 20 GPIOs at once"""
    GP    = range(2,22)
    GS_on = [0]*len(GP)
    GPIO.output(GP,GS_on)
    print("all_off")
    return 0

if sys.argv[1] == "test":
   lanetest()
elif sys.argv[1] == "on":
   all_on()
else:
   all_off()
