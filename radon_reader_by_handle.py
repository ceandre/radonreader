import bluepy.btle as btle
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


##50 0a 02 00 05 00 00 00 00 00 00 00
##02 05 00 00 05 00 00 00 00'
##b'P\n\x02\x00\x05\x00\x00\x00\x00\x00\x00\x00'


	
class ReadDelegate(btle.DefaultDelegate):
    def handleNotification(self, cHandle, data):
        RadonValue = struct.unpack('<H',data[2:4])[0]
        logger.debug('Radon Value Raw: {}'.format(data))
        logger.debug('Radon Value Bq/m^3: {}'.format(RadonValue))
        RadonValue = ( RadonValue / 37 )
        logger.debug('Radon Value pCi/L: {}'.format(RadonValue))

p = btle.Peripheral("94:3c:c6:dd:42:ce")
p.withDelegate(ReadDelegate())

#send -- "char-write-cmd 0x002a 50\r"
intHandle = int.from_bytes(b'\x00\x2a', "big")
bGETValues = b"\x50"

p.writeCharacteristic(intHandle, bGETValues, True);

while True:
    while p.waitForNotifications(1):
        pass
p.disconnect()



