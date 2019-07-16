#!/usr/bin/python
#
# RadonEye RD200 Reader (Bluetooth/BLE)
#
# Author: Carlos Andre
#
 
import struct
import time

from bluepy import btle
from time import sleep

# Put here your RadonEye Bluetooth Address
RadonEyeBTAddress = "E4:34:1D:xx:xx:xx"

# Choose Unit of Measurement - pCi/L (True) or Bq/m^3 (False)
picoCurie = True

# Verbose - Enable (True) or Disable (False)
Verbose = False

# Output - Only Radon Value or Full (timestamp and Unit)
OnlyValue = False

def GetRadonValue():

    if Verbose: 
        print ("Connecting...")
    DevBT = btle.Peripheral(RadonEyeBTAddress, "random")
    RadonEye = btle.UUID("00001523-1212-efde-1523-785feabcd123")
    RadonEyeService = DevBT.getServiceByUUID(RadonEye)

    # Write 0x50 to 00001524-1212-efde-1523-785feabcd123
    if Verbose: 
        print ("Writing...")
    uuidWrite  = btle.UUID("00001524-1212-efde-1523-785feabcd123")
    RadonEyeWrite = RadonEyeService.getCharacteristics(uuidWrite)[0]
    RadonEyeWrite.write(bytes("\x50"))

    # Read from 2nd to 6th byte of 00001525-1212-efde-1523-785feabcd123
    if Verbose: 
        print ("Reading...")
    uuidRead  = btle.UUID("00001525-1212-efde-1523-785feabcd123")
    RadonEyeValue = RadonEyeService.getCharacteristics(uuidRead)[0]
    RadonValue = RadonEyeValue.read()
    RadonValue = struct.unpack('<f',RadonValue[2:6])[0]
   
    if picoCurie:
        Unit="pCi/L"
    else:
        Unit="Bq/m^3"
        RadonValue = RadonValue * 37
 
    if OnlyValue:
        print ("%0.2f" % (RadonValue))
    else: 
        print ("%s - Radon Value: %0.2f %s" % (time.strftime("%Y-%m-%d [%H:%M:%S]"),RadonValue,Unit))
    
try:
    GetRadonValue()
except:
    if Verbose: 
        print ("Connection failed, trying again...")
    sleep(5)

    try: 
        GetRadonValue()
    except:
        print ("Connection failed.")
