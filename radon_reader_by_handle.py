#!/usr/bin/python3
import bluepy.btle as btle
from bluepy.btle import Scanner, DefaultDelegate, BTLEException
import struct
import logging
import sys
from time import sleep


logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)


class ScanDelegate(DefaultDelegate):
	def __init__(self):
		DefaultDelegate.__init__(self)

	def handleDiscovery(self, dev, isNewDev, isNewData):
		pass

def radon_device_finder():
	logger.debug('Scanning for devices')
	scanner = Scanner().withDelegate(ScanDelegate())
	try:
		devices = scanner.scan(10.0)
		for device in devices:
			name = ''
			if device.getValueText(9):
				name = device.getValueText(9)
			elif device.getValueText(8):
				name = device.getValueText(8)
			logger.debug('Device name: ' + name)
			if 'FR:RU' in name:
				logger.info('Found RD200 - x>=2022 revision with address: ' + device.addr)
				return device.addr, 1
			elif 'FR:R2' in name:
				logger.info('Found RD200 - x<2002 revision with address: ' + device.addr)
				return device.addr, 0
		logger.info('Finished scanning for devices, no devices found')
		return "", -1
	except BTLEException as e:
		scanner.stop()
		logger.error('Recieved scan exception ' + e.message)

#raw data for .05 pCi/L:
##50 0a 02 00 05 00 00 00 00 00 00 00
##02 05 00 00 05 00 00 00 00'
##b'P\n\x02\x00\x05\x00\x00\x00\x00\x00\x00\x00'

radonDataRAW = b"\x00"
class ReadDelegate(btle.DefaultDelegate):
	def handleNotification(self, cHandle, data):
		global radonDataRAW
		logger.debug('Radon Value Raw: {}'.format(data))
		radonDataRAW=data

def nConnect(per, num_retries, address):
        try_num = 1
        while (try_num < num_retries):
            try:
                per._connect(address)
                return True
            except BTLEException:
                logger.debug("Re-trying connections attempts: {}'".format(try_num))
                try_num += 1
                sleep(1)
        # if we fell through the while loop, it failed to connect
        return False 

def radon_device_reader(rdDeviceAddress,rdDeviceType):
	if rdDeviceType >= 0:
		p = btle.Peripheral()
		nConnect(p, 5, rdDeviceAddress);
		p.withDelegate(ReadDelegate())
		#send -- "char-write-cmd 0x002a 50\r" ./temp_expect.sh  (https://community.home-assistant.io/t/radoneye-ble-interface/94962/115)

		if rdDeviceType == 1:
			#handle: 0x002a, uuid: 00001524-0000-1000-8000-00805f9b34fb 
			intHandle = int.from_bytes(b'\x00\x2a', "big")
		elif rdDeviceType == 0:  #old
			#handle: 0x000b, uuid: 00001524-1212-efde-1523-785feabcd123
			intHandle = int.from_bytes(b'\x00\x0b', "big") 

		bGETValues = b"\x50"

		logger.debug('Sending payload (byte): %s To handle (int): %s', bGETValues, intHandle)
		p.writeCharacteristic(intHandle, bGETValues, True);
		while p.waitForNotifications(1):
        		pass
		p.disconnect()

		if rdDeviceType == 1: #new RD200 sends back short int (2-bytes) with Bq/m^3
			RadonValueBQ = struct.unpack('<H',radonDataRAW[2:4])[0]
			RadonValuePCi = ( RadonValueBQ / 37 )
		elif rdDeviceType == 0:  #old RD200 sends back pCi/L as a 4-byte float
			RadonValuePCi = struct.unpack('<f',radonDataRAW[2:6])[0]
			RadonValueBQ = ( RadonValuePCi * 37 )
		logger.info('Radon Value Bq/m^3: {}'.format(RadonValueBQ))
		logger.info('Radon Value pCi/L: {}'.format(RadonValuePCi))

		return RadonValueBQ, RadonValuePCi

	elif rdDeviceType == -1:
		logger.error("Device not found, no data to return.")
		return  -1,-1


#testing w/o radon_reader.py

if ('radon_reader_by_handle' not in sys.modules): #if I was not imported

	logger.addHandler(handler) # add handler for standard out

	mRdDeviceAddress, mRdDeviceType = radon_device_finder() #auto find the device
	radon_device_reader (mRdDeviceAddress , mRdDeviceType) #get data from the device


