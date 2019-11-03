from datetime import date, datetime, timedelta
import time
import RPi.GPIO as GPIO
import signal

def split_str(word):
    return [int(char) for char in word]

def get_day_nr():
    NOW  = datetime.now()-timedelta(hours=9)  ### current
    YEAR = NOW.year
    S    = date(YEAR,1,1)
    E    = date(YEAR, NOW.month, NOW.day)
    return str(YEAR)[2:],str((E-S).days)

def get_4bit(YearDay):
    Y, D   = YearDay
    STRING = split_str(Y)+split_str(D)
    LIST=[]
    for i in STRING:
        DY = bin(i)[2:].zfill(4)
        LIST+=split_str(DY)

    return LIST

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    GS_off = [0]*len(GP)
    GPIO.output(GP,GS_off)
    exit(0)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GP = range(2,22)
GPIO.setup(GP, GPIO.OUT)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

while True:

    GS_off = [0]*len(GP)
    GS_on  = [1]*len(GP)

    YEAR, DAY = get_day_nr()
    GS        = get_4bit([YEAR, DAY])

    ##### set pin mode
    """
    for i in GP:
        GPIO.setup(i, GPIO.OUT)
    """
    
    print "+"*25
    print "DATE"
    print datetime.now()
    print "-"*25
    print "GMT"
    print datetime.now()-timedelta(hours=9)
    print "-"*25
    print YEAR, DAY
    print "-"*25
    print GS

    GPIO.output(GP,GS)
    
    time.sleep(1)


    
