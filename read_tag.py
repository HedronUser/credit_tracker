import time
import serial
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
 
Tag1 = str('1800387799CE')
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.output(23,False)
GPIO.output(24,False)
PortRF = serial.Serial('/dev/ttyAMA0',9600)
while True:
    ID = ""
    read_byte = PortRF.read()
    if read_byte=="\x02":
        for Counter in range(12):
            read_byte=PortRF.read()
            ID = ID + str(read_byte)
            print hex(ord( read_byte))
        print ID
        if ID == Tag1:
            print "matched"
            GPIO.output(23,True)
            GPIO.output(24,False)
            time.sleep(5)
            GPIO.output(23,False)
        else:
            GPIO.output(23,False)
            print "Access Denied"
            GPIO.output(24,True)
            time.sleep(5)
            GPIO.output(24,False)
