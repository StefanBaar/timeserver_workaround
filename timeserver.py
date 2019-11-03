from datetime import date, datetime, timedelta
import time
import RPi.GPIO as GPIO
import signal

import serial

PORT = "/dev/ttyACM0"


def split_str(word):
    """Splits string into integers and return them within a list
       Input: String
       Output: List """
    return [int(char) for char in word]

def get_day_nr():
    """Returns year and number of days.
       Output: int, int <-- Year, Days"""
    NOW  = datetime.now()-timedelta(hours=9)  ### current time
    YEAR = NOW.year
    S    = date(YEAR,1,1)
    E    = date(YEAR, NOW.month, NOW.day+1)
    return str(YEAR)[2:],str((E-S).days)

def get_4bit(YearDay):
    """Converts integer of Year and Days into List of binaries.
       Output: List, with 20 elements"""
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

def set_relay(LIST):
    """switch relays according to LIST.
       Input: List, 20 elements"""

    portName=PORT   ### required usb port number of the relay, can be found in /dev/

    def compute_relay(relayNum):
        """Return nameing relay names from numbers."""
        if (int(relayNum) < 10):
           relayIndex = str(relayNum)
        else:
           relayIndex = chr(55 + int(relayNum))

        return relayIndex

    serPort = serial.Serial(portName, 19200, timeout=1)

    for i in range(len(LIST)):
        if LIST[i]==1:
            relayCmd = "on"
        else:
            relayCmd = "off"

        relayIndex=compute_relay(i)
        serPort.write("relay "+ str(relayCmd) +" "+ relayIndex + "\n\r")

    serPort.close()
    return 0

# setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GP = range(2,22)
GPIO.setup(GP, GPIO.OUT)

#signal.signal(signal.SIGINT, keyboardInterruptHandler)

while True:

    GS_off = [0]*len(GP)              ### set a sequence of 20 to all off/ 0
    GS_on  = [1]*len(GP)              ### set a sequence of 20 of all on/1

    YEAR, DAY = get_day_nr()          ### get year and number of days since beginning of the year
    GS        = get_4bit([YEAR, DAY]) ### convert YEAR and Day number to reaveled List of 5x4bit binaries
    GSI       = GS[:8][::-1]+GS[8:][::-1]
    ##### set pin mode
    """
    for i in GP:
        GPIO.setup(i, GPIO.OUT)
    """

    print ("+"*25)
    print ("DATE")
    print (datetime.now())
    print ("-"*25)
    print ("GMT")
    print (datetime.now()-timedelta(hours=9))
    print ("-"*25)
    print ("Year, Day converted to ports:")
    print (YEAR, DAY)
    print ("-"*25)
    print ("4bit bins")
    print (GS)
    print ("-"*25)
    print ("4bit bins port ordered ")
    print (GSI)

    set_relay(GSI)            ### set the relays according to sequence GS
    GPIO.output(GP,GSI)       ### set GPIO according to sequence GS

    time.sleep(1)
