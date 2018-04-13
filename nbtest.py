import time
import serial
import SDL_Pi_HDC1000
#import Adafruit_DHT
import ADS1x15 as Adafruit_ADS1x15
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

#Relay
relay = 26
gpio.setup(relay,gpio.OUT)

gpio.output(relay,gpio.HIGH)
time.sleep(2)
gpio.output(relay,gpio.LOW)
time.sleep(1)

#User LED

userled = 20
gpio.setup(userled,gpio.OUT)
gpio.output(userled,gpio.HIGH)
time.sleep(2)
gpio.output(userled,gpio.LOW)
time.sleep(1)

#ADS1X15

adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)
GAIN = 1

print('Channel 0: {0}'.format(adc.read_adc(2, gain=GAIN)))

# DHT.AM2302

#sensor = Adafruit_DHT.AM2302
#pin = 4

#ambientHumidity, ambientTemperature = Adafruit_DHT.read_retry(sensor, pin)

#print "Ambient Humidity : %d " % ambientHumidity
#print "Ambient Temperature : %d " % ambientTemperature


# HDC1080

hdc1000 = SDL_Pi_HDC1000.SDL_Pi_HDC1000()

print "turning Heater On" 
hdc1000.turnHeaterOn() 

# turn heater off
print "turning Heater Off"
hdc1000.turnHeaterOff() 

print "change temperature resolution"
hdc1000.setTemperatureResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_TEMPERATURE_RESOLUTION_14BIT)
# read configuration register
print "configure register = 0x%X" % hdc1000.readConfigRegister()

print "change humidity resolution"
hdc1000.setHumidityResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_HUMIDITY_RESOLUTION_14BIT)
# read configuration register
print "configure register = 0x%X" % hdc1000.readConfigRegister()

cabinateTemperature = hdc1000.readTemperature();
cabinateHumidity = hdc1000.readTemperature();

print "Cabinate Humidity : %d " % cabinateHumidity
print "Cabinate Temperature : %d " % cabinateTemperature
        

#print ('{{"_0":{0}, "_1":{1}, "_2":{2}, "_3":{3}, "_4":{4}}}'.format(ambientHumidity, ambientTemperature, cabinateTemperature, cabinateHumidity, adc.read_adc(2, gain=1)))


# configure the serial connections (the parameters differs on the device you are connecting to)
ser=serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

while 1:

	ser.reset_input_buffer()

   	while 1:
        	ser.write("AT+NRB\r")
        	time.sleep(1)
        	response = ser.readline()
        	response = ser.readline()
        	print 'RESPONSE:%s' % response

        	if response.startswith('OK'):
        		break

    	print 'TAMAMLANDI 0'



    	ser.reset_input_buffer()



    	while 1:
		ser.write("AT+CGATT?\r")
        	time.sleep(1)

        	while 1:	

            		ser.write("AT+CGATT=1\r")
		        time.sleep(1)
            		ser.reset_input_buffer()
            		ser.write("AT+CGATT?\r")
	        	time.sleep(1)
            		response = ser.readline()
            		response = ser.readline()
            		print 'RESPONSE:%s' % response

		        if response.startswith('+CGATT:1'):
                		break

		break

	print 'TAMAMLANDI 4'

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

    	print 'TAMAMLANDI 5'
    	break


while 1:
	
	while 1:
		print 'NUESTATS CHECKING'
		ser.reset_input_buffer()
	        signal = 0

        	while 1:
 	        	ser.write("AT+NUESTATS\r")
			time.sleep(3)

            		while 1:
                		response = ser.readline()
                		print 'RESPONSE:%s' % response

                		if response.startswith('Signal power:'):
	                    		signal = int(response.split(':',2)[1])/10

                		if response.startswith('OK'):
                    			break

                		time.sleep(0.1)
			break

	#ambientHumidity, ambientTemperature = Adafruit_DHT.read_retry(sensor, pin)

        	data = '{{"_0":{0}, "_1":{1}, }}'.format( hdc1000.readTemperature(), hdc1000.readHumidity())

        	print data
        	print 'DATA SENDING'
        	data ='AT+NSOST=0,78.182.61.201,5000,{0},{1}\r'.format(str(len(data)),data.encode("hex"))
	#78.182.61.201 is ip of router and 5000 isthe enabled port. 
        	ser.reset_input_buffer()
        	ser.write(data)
        	response = ser.readline()
        	response = ser.readline()
        	print 'RESPONSE:%s' % response
        	time.sleep(5)


		print 'FULL OK'
adc.stop_adc()  


