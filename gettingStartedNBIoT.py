import time
#from threading import Timer
import urllib2
#import datetime
import serial

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)


def wait():
	sixfab.toggleLed()
	time.sleep(0.3)
	
while 1:

	ser.reset_input_buffer()
	while 1:
		ser.write("ATE1\r")
		time.sleep(1)
		response = ser.readline()
		response = ser.readline()
		print 'RESPONSE:%s' % response	
		if response.startswith('OK'):
			break
	print 'DONE 0'
	ser.reset_input_buffer()
	
	while 1:
		ser.write("AT+CFUN=1\r")
		time.sleep(1)
		response = ser.readline()		
		response = ser.readline()
		print 'RESPONSE:%s' % response
		if response.startswith('OK'):
			break
	print 'DONE 1'
	ser.reset_input_buffer()

	while 1:
		ser.write("AT+CGATT=1\r")
		time.sleep(0.5)
		response = ser.readline()		
		response = ser.readline()
		print 'RESPONSE:%s' % response
		if response.startswith('OK'):
			break
	print 'DONE 2'
	ser.reset_input_buffer()

	while 1:
		ser.write("AT+CGDCONT=1,\"IP\",\"IOTTEST\"\r")
		time.sleep(1)
		response = ser.readline()		
		response = ser.readline()
		print 'RESPONSE:%s' % response
		if response.startswith('OK'):
			break

	print 'DONE 3'
	time.sleep(3)
	ser.reset_input_buffer()
	while 1:
		ser.write("AT+CGATT?\r")
		time.sleep(1)
		while 1:
			ser.write("AT+CGATT?\r")
			time.sleep(1)
			response = ser.readline()
			response = ser.readline()
			print 'RESPONSE:%s' % response
			if response.startswith('+CGATT:1'):
				break
		break
	print 'DONE 4'
	ser.write('AT+NSOCL=0\r')
	time.sleep(1)
	ser.reset_input_buffer()
	while 1:
		ser.write("AT+NSOCR=DGRAM,17,3005,1\r")
		time.sleep(0.5)
		while 1:
			response = ser.readline()
			response = ser.readline()
			print 'RESPONSE:%s' % response
		
			if response.startswith('OK'):
				break
				
			if response.startswith('ERROR'):
				ser.write("AT+NSOCR=DGRAM,17,3005,1\r")
			
		break

	print 'DONE 5'
	
	break


while 1:
 
	data = 'SIXFAB NB-IoT\n'
	print data
		
        print 'DATA SENDING'
        
        data ='AT+NSOST=0,78.182.61.201,5000,{0},{1}\r'.format(str(len(data)),data.encode("hex"))
        ser.reset_input_buffer()
	ser.write(data)
        
        response = ser.readline()
        response = ser.readline()
        print 'RESPONSE:%s' % response
        time.sleep(2)
