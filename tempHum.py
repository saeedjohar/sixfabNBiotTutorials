##
##
##Basic Tutorial SIXFAB NB-IoT SHIELD
##Reading temperature and humidity 
##
##
import time
import serial
import SDL_Pi_HDC1000


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
 	#Data formatting
	temperature = hdc.readTemperature()
	humidity = hdc.readHumidity()
	data = '{{Temperature:{0}, Humidity:{1}}}\n'.format(temperature, humidity)
	print data
		
        print 'DATA SENDING'
        ## IMPORTANT: Router's IP and UDP port information to be edit here
        data ='AT+NSOST=0,85.109.205.164,5500,{0},{1}\r'.format(str(len(data)),data.encode("hex"))
        ser.reset_input_buffer()
	ser.write(data)
        
        response = ser.readline()
        response = ser.readline()
        print 'RESPONSE:%s' % response
        time.sleep(2)
