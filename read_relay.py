import sys
import serial

if (len(sys.argv) < 2):
	print("Usage: relayread.py <PORT> <RELAYNUM>\nEg: relayread.py COM1 0")
	print("WINDOWS: COM1, UNIX: /dev/tty.ACM0, MAC: /dev/tty.usb...")
	sys.exit(0)
else:
	portName = sys.argv[1];
	relayNum = sys.argv[2];

#Open port for communication
serPort = serial.Serial(portName, 19200, timeout=1)

if (int(relayNum) < 10):
    relayIndex = str(relayNum)
else:
    relayIndex = chr(55 + int(relayNum))

serPort.write("relay read "+ relayIndex + "\n\r")

response = serPort.read(25)

if(response.find("on") > 0):
	print("Relay " + str(relayNum) +" is ON")

elif(response.find("off") > 0):
	print("Relay " + str(relayNum) +" is OFF")

#Close the port
serPort.close()
