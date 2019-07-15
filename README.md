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
  - <b>RadonEyeBTAddress</b> = "xx:xx:xx:xx:xx:xx"
    - Your RadonEye RD200 Bluetooth Address
  - <b>picoCurie</b> = <i>True</i> or <i>False</i>
    - Shows Radon Level on pCi/L unit if <b>True</b>, or Bq/m^3 unit if <b>False</b>
  - <b>Verbose</b> = <i>True</i> or <i>False</i>
    - Verbose mode (on / off)
  - <b>OnlyValue</b> = <i>True</i> or <i>False</i>
    - Show only radon value without timestamp and unit information
    
    
