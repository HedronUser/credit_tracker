#!/usr/bin/python2
import serial
import re, sys, signal, os, time, datetime
import RPi.GPIO as GPIO

BITRATE = 9600
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
#GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Lock the door on boot
GPIO.output(23, GPIO.LOW)

#pidfile = daemon.pidfile.PIDLockFile("/var/run/bearclaw.pid")

#fill dictionary with tag UID numbers as keys and purchased minutes as values
credit_dict = { '0007421597': 0, '1512305969': 0,  '0007394263': 60, '0007406707': 0, '0007411862': 0, '0007395322': 0, '0007410979': 0, '0007416591':0, '0007398453':0}

#credit_dict should eventually be ported to retrieve from a database that is updated automatically

CARDS = [
'060090840715',
'840034BD3E33',
'6A003E3A2C42',
'840034D5DDB8',
'6A003E6F556E',
'840034CD324F',
'6A003E61AC99',
'6A003E247E0E',
'6A003E77BD9E',
'840034D6CEA8'
]

def signal_handler(signal, frame):
  print "Shutting Down Laser"
  GPIO.output(23, GPIO.LOW)  # lock the laser on program exit
  GPIO.cleanup()
  ser.close()
  sys.exit(0)

def unlock_tool(duration):
  print "Unlocking tool for %d seconds" % duration
  GPIO.output(23, GPIO.HIGH)
  time.sleep(duration)
  print "Locking the tool"
  GPIO.output(23, GPIO.LOW)

if __name__ == '__main__':
    buffer = ''
    ser = serial.Serial('/dev/ttyAMA0', BITRATE, timeout=0)
    rfidPattern = re.compile(b'[\W_]+')
    signal.signal(signal.SIGINT, signal_handler)

    while True:
      # Read data from RFID reader
      buffer = buffer + ser.read(ser.inWaiting())
      if '\n' in buffer:
        lines = buffer.split('\n')
        last_received = lines[-2]
        match = rfidPattern.sub('', last_received)

        if match:
          print str(match)
          if str(match) in credit_dict.keys():
            print 'card authorized'
            unlock_tool(10) #replace the number ten with their minutes purchased
            print "verifying with server"  
          else:
            print 'unauthorized card'
          
        #insert code for server verification
            
        # Clear buffer
        buffer = ''
        lines = ''

      # Listen for Exit Button input
##      if not GPIO.input(3):
##        print "button pressed"
##        unlock_door(5)

      time.sleep(0.1)
