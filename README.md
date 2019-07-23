# RadonReader

This project provides a tool which allows users collect current radon data from FTLab Radon Eye RD200 (Bluetooth only version).

# Hardware Requeriments
- FTLabs RadonEye RD200 
- Raspberry Pi 
- Bluetooth with BLE (Low Energy) support

# Software Requeriments
- Python 2.7.x 
- bluepy Python library

# Usage
<pre><code>radon_reader.py [-h] -a ADDRESS [-b] [-v] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        Bluetooth Address (AA:BB:CC:DD:EE:FF format)
  -b, --becquerel       Display radon value in Becquerel (Bq/m^3) unit
  -v, --verbose         Verbose mode
  -s, --silent          Only output radon value (without unit and timestamp)
 </code></pre>
