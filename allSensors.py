##
##
##Intermediate Tutorial SIXFAB NB-IoT SHIELD
##Reading data from all sensors 
##
##
import time
import serial
import SDL_Pi_HDC1000
import Adafruit_ADS1x15
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

#Relay
relay = 26
print"RELAY TEST"
gpio.setup(relay,gpio.OUT)
gpio.output(relay,gpio.HIGH)
time.sleep(1)
gpio.output(relay,gpio.LOW)
time.sleep(0.5)

#USER LED

led = 20 
print"LED TEST"
gpio.setup(led,gpio.OUT)
gpio.output(led,gpio.HIGH)
time.sleep(1)
gpio.output(led,gpio.LOW)
time.sleep(0.5)

#ADS1X15

adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)
GAIN = 1

#print('Channel 0: {0}'.format(adc.read_adc(2, gain=GAIN)))
print "ALL CHANNEL"
for i in range(4):
        print adc.read_adc(i, gain=GAIN)

#Lux
LUXCHANNEL = 0
rawLux = adc.read_adc(LUXCHANNEL,gain=GAIN)
lux = (rawLux * 100)/1580
print "LUX: %d" %lux
#Tempertaure and Humidity

hdc = SDL_Pi_HDC1000.SDL_Pi_HDC1000()

temperature = hdc.readTemperature()
humidity = hdc.readHumidity()

#Prints as integer
print "Temperature: %d" %temperature
print "Humidity: %d" %humidity

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)


	
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
#	print 'DONE 0'
	ser.reset_input_buffer()
	
	while 1:
		ser.write("AT+CFUN=1\r")
		time.sleep(1)
		response = ser.readline()		
		response = ser.readline()
		print 'RESPONSE:%s' % response
		if response.startswith('OK'):
			break
#	print 'DONE 1'
	ser.reset_input_buffer()

	while 1:
		ser.write("AT+CGATT=1\r")
		time.sleep(0.5)
		response = ser.readline()		
		response = ser.readline()
		print 'RESPONSE:%s' % response
		if response.startswith('OK'):
			break
#	print 'DONE 2'
	ser.reset_input_buffer()

	while 1:
		ser.write("AT+CGDCONT=1,\"IP\",\"IOTTEST\"\r")
		time.sleep(1)
		response = ser.readline()		
		response = ser.readline()
		print 'RESPONSE:%s' % response
		if response.startswith('OK'):
			break

#	print 'DONE 3'
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
#	print 'DONE 4'
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

#	print 'DONE 5'
	
	break


while 1:

	temp = hdc.readTemperature()
	hum = hdc.readHumidity()
	rawLux = adc.read_adc(0,gain=GAIN)
	lux = (adc.read_adc(LUXCHANNEL,gain=GAIN) * 100)/1580
 	#Data formatting
	data = '{{Temperature:{0}, Humidity:{1}, Lux:{2}}}\n'.format(temp, hum, lux)
	print data
		
        print 'DATA SENDING'
        ## IMPORTANT: Router's IP and UDP port information to be edit here
        data ='AT+NSOST=0,78.182.58.240,5500,{0},{1}\r'.format(str(len(data)),data.encode("hex"))
        ser.reset_input_buffer()
	ser.write(data)
        
        response = ser.readline()
        response = ser.readline()
        print 'RESPONSE:%s' % response
        time.sleep(2)
