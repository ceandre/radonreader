# RadonReader 2022 RD200 v2 (=>2022)


EtoTen v0.4 - 07/05/2022
- Forked Project
- Changed compatability to Python3 
- Added support for new RD200 models made in 2022
- Added auto-scan ability 
- Change the read function to call the handler directly, instead of interacting with the UUIDs

Note: if specifying an (-a) MAC address, you now also have to specify a device type (-t) (either 0 for original RD200 or 1 for RD200 v2)


# Pre-req install steps:

<pre><code>
sudo apt install libglib2.0-dev
pip3 install bluepy
pip3 install paho-mqtt
sudo setcap cap_net_raw+e /home/pi/.local/lib/python3.7/site-packages/bluepy/bluepy-helper
sudo setcap cap_net_admin+eip /home/pi/.local/lib/python3.7/site-packages/bluepy/bluepy-helper
</pre></code>


------------

This project provides a tool which allows users collect current radon data from FTLab Radon Eye RD200 (Bluetooth only version).


# Hardware Requirements
- FTLabs RadonEye RD200 v1 or v2
- Raspberry Pi w/Bluetooth LE (Low Energy) support (RPi 3B/4/etc...)

# Software Requirements
- Python 3.7
- bluepy Python library
- paho-mqtt Python library

# History
- 0.4 - Forked
- 0.3 - Added MQTT support


# Usage
<pre><code>usage: radon_reader.py [-h] [-a] ADDRESS [-t] DEVICE_TYPE [-b] [-v] [-s] [-m] [-ms MQTT_SRV]
                       [-mp MQTT_PORT] [-mu MQTT_USER] [-mw MQTT_PW] [-ma]

RadonEye RD200 (Bluetooth/BLE) Reader

optional arguments:
  -h, --help       show this help message and exit
  -a ADDRESS       Bluetooth Address (AA:BB:CC:DD:EE:FF format)
  -t TYPE          0 for original RD200, 1 for RD200 v2 (=>2022)
  -b, --becquerel  Display radon value in Becquerel (Bq/m^3) unit
  -v, --verbose    Verbose mode
  -s, --silent     Only output radon value (without unit and timestamp)
  -m, --mqtt       Enable send output to MQTT server
  -ms MQTT_SRV     MQTT server URL or IP address
  -mp MQTT_PORT    MQTT server service port (Default: 1883)
  -mu MQTT_USER    MQTT server username
  -mw MQTT_PW      MQTT server password
  -ma              Enable Home Assistant MQTT output (Default: EmonCMS)</code></pre>

# Example usage:
<pre><code>
python3 radon_reader.py -a 94:3c:c6:dd:42:ce -t 1 -v
python3 radon_reader.py -v
</pre></code>
