import sys
import serial

def compute_relay(relayNum):
        """Return nameing relay names from numbers.
        INPUT:  integer
        OUTPUT: integer"""

        if (int(relayNum) < 10):
           relayIndex = str(relayNum)
        else:
           relayIndex = chr(55 + int(relayNum))

        return relayIndex

if (len(sys.argv) < 2):
	print("Usage: relaywrite.py <PORT> <RELAYNUM> <CMD>\nEg: relaywrite.py COM1 0 on")
	print("WINDOWS: COM1, UNIX: /dev/tty.ACM0, MAC: /dev/tty.usb...")
	sys.exit(0)
else:
	portName = sys.argv[1];
	relayNum = sys.argv[2];
	relayCmd = sys.argv[3];

#Open port for communication
serPort = serial.Serial(portName, 19200, timeout=1)

#Compute relay number
relayNum = compute_relay(relayNum)

#Send the command

serPort.write("relay "+ str(relayCmd) +" "+ str(relayNum) + "\n\r")

print("Command sent...")

#Close the port
serPort.close()
