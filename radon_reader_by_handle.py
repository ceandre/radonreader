import bluepy.btle as btle
from bluepy.btle import Scanner, DefaultDelegate, BTLEException
import struct
import logging
import sys

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class ScanDelegate(DefaultDelegate):
	def __init__(self):
		DefaultDelegate.__init__(self)

	def handleDiscovery(self, dev, isNewDev, isNewData):
		pass

def radeon_device_finder():
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



class ReadDelegate(btle.DefaultDelegate):
	def handleNotification(self, cHandle, data):
		if rdDeviceType == 1: #new RD200 sends back short int (2-bytes) with Bq/m^3
			RadonValueBQ = struct.unpack('<H',data[2:4])[0]
			logger.debug('Radon Value Raw: {}'.format(data))
			RadonValuePCi = ( RadonValueBQ / 37 )

		elif rdDeviceType == 0:  #old RD200 sends back pCi/L as a 4-byte float
			RadonValuePCi = struct.unpack('<f',data[2:6])[0]
			logger.debug('Radon Value Raw: {}'.format(data))
			RadonValueBQ = ( RadonValuePCi * 37 )

		logger.info('Radon Value Bq/m^3: {}'.format(RadonValueBQ))
		logger.info('Radon Value pCi/L: {}'.format(RadonValuePCi))

#raw data for .05 pCi/L:
##50 0a 02 00 05 00 00 00 00 00 00 00
##02 05 00 00 05 00 00 00 00'
##b'P\n\x02\x00\x05\x00\x00\x00\x00\x00\x00\x00'


rdDeviceAddress, rdDeviceType = radeon_device_finder() #auto find the device

if rdDeviceType >= 0:
	p = btle.Peripheral(rdDeviceAddress)
	p.withDelegate(ReadDelegate())

	#send -- "char-write-cmd 0x002a 50\r"
	intHandle = int.from_bytes(b'\x00\x2a', "big")
	bGETValues = b"\x50"
	logger.debug('Sending payload (byte): %s To handle (int): %s', bGETValues, intHandle)
	p.writeCharacteristic(intHandle, bGETValues, True);

	while p.waitForNotifications(1):
        	pass
	p.disconnect()

elif rdDeviceType == -1:
	logger.error("Device not found, no data to return.")

