# RadonReader

This project provides a tool which allows users collect currect radon data from FTLab Radon Eye RD200 (Bluetooth only version).

# Limitations

For now you must configure the file directly.

# Hardware Requeriments
- FTLabs RadonEye RD200 
- Raspberry Pi 
- Bluetooth with BLE (Low Energy) support

# Software Requeriments
- Python 2.7.x 
- bluepy Python library

# Using

- Open radonreader.py and configure it directly. 
  - <b>RadonEyeBTAddress</b> = [your RD200 Bluetooth Address]
  - <b>picoCurie</b> = <i>True</i> or <i>False</i>
    Shows Radon Level on pCi/L unit if True, or Bq/m^3 unit if False
  - Verbose = <i>True</i> or <i>False</i>
  - OnlyValue = <i>True</i> or <i>False</i>
    Show only radon value without unit information
    
    
