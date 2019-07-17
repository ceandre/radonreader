#!/usr/bin/python

""" radon_reader.py: RadonEye RD200 (Bluetooth/BLE) Reader """

__progname__    = "RadonEye RD200 (Bluetooth/BLE) Reader"
__version__     = "0.2"
__author__      = "Carlos Andre"
__email__       = "candrecn at hotmail dot com"
__date__        = "2019-07-17"

import argparse, struct, time, re

from bluepy import btle
from time import sleep

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description=__progname__)
parser.add_argument('-a','--address',help='Bluetooth Address (AA:BB:CC:DD:EE:FF format)',required=True)
parser.add_argument('-b','--becquerel',action='store_true',help='Display radon value in Becquerel (Bq/m^3) unit', required=False)
parser.add_argument('-v','--verbose',action='store_true',help='Verbose mode', required=False)
parser.add_argument('-s','--silent',action='store_true',help='Only output radon value (without unit and timestamp)', required=False)
args = parser.parse_args()

if not re.match("[0-9a-f]{2}(:?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", args.address.lower()):
    parser.print_help()
    quit()

def GetRadonValue():
    if args.verbose and not args.silent:
        print ("Connecting...")
    DevBT = btle.Peripheral(args.address.upper(), "random")
    RadonEye = btle.UUID("00001523-1212-efde-1523-785feabcd123")
    RadonEyeService = DevBT.getServiceByUUID(RadonEye)

    # Write 0x50 to 00001524-1212-efde-1523-785feabcd123
    if args.verbose and not args.silent:
        print ("Writing...")
    uuidWrite  = btle.UUID("00001524-1212-efde-1523-785feabcd123")
    RadonEyeWrite = RadonEyeService.getCharacteristics(uuidWrite)[0]
    RadonEyeWrite.write(bytes("\x50"))

    # Read from 2nd to 6th byte of 00001525-1212-efde-1523-785feabcd123
    if args.verbose and not args.silent:
        print ("Reading...")
    uuidRead  = btle.UUID("00001525-1212-efde-1523-785feabcd123")
    RadonEyeValue = RadonEyeService.getCharacteristics(uuidRead)[0]
    RadonValue = RadonEyeValue.read()
    RadonValue = struct.unpack('<f',RadonValue[2:6])[0]
   
    if args.becquerel:
        Unit="Bq/m^3"
        RadonValue = ( RadonValue * 37 )
    else:
        Unit="pCi/L"
 
    if args.silent:
        print ("%0.2f" % (RadonValue))
    else: 
        print ("%s - %s - Radon Value: %0.2f %s" % (time.strftime("%Y-%m-%d [%H:%M:%S]"),args.address.upper(),RadonValue,Unit))
    
try:
    GetRadonValue()
except:
    for i in range(1,4):
        try:
            if args.verbose and not args.silent:
                print ("Connection failed, trying again (%s)..." % i)
            sleep(5)
            GetRadonValue()
        except:
            if i < 3:
                continue
            else:
                print ("Connection failed.")
        break

