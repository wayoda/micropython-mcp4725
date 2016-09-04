# micropython-mcp4725
A [micropython](http://micropython.org) driver for the MCP4725 I²C DAC.

The MCP4725 is a digital to analog converter chip with a 12-Bit resolution on
the output. The MCP4725 works with a supply voltage from 3.3V to 5V. The output  
range is from 0V up to the supply voltage. 

The MCP4725 can be configured to two different addresses (0x62,0x63) on the I²C bus.
That way it is possible to use 2 MCP4725 on any I²C bus. The device supports
standard (100kbps) and fast (400kbps) and hi-speed (3.4Mbps) bus speeds. But
hi-speed seems not to be supported by any of the micropython hardware boards.
The fast baudrate of 400kbps works fine with the 
[WiPy](https://www.pycom.io/solutions/py-boards/wipy/) but compared with DACs
that are connected to a SPI-bus the MCP4725 update on the output voltage are pretty slow.

The MCP4725 supports 3 different power-down modes where the output voltage
driver shuts down and the device goes to sleep to save energy. The cips wakes up
from power-down mode whenever a output voltage update is send to the device.

The MCP4725 also has a small eeprom where the power-down mode and the initial
output voltage can be configured that are to be used when the MCP4725 is powered
up.

##Using the MCP4725 in your micropython project
There are only a lines of code needed if you want add a MCP4725 to your project.

###Create and initialze the I²C bus of your micropython board
A micropython driver for an I²C device expects the you create and initialze a
``machine.I2C`` instance and pass the to your drivers constructor.

The arguments in the code example work for a WiPy board. If you try this with a
different board please check the pins to use for the I²C bus. 

```python

from machine import I2C
from mcp4725 import MCP4725

#create a I2C bus
i2c=I2C(0,I2C.MASTER,baudrate=400000,pins=('GP15','GP14')) 

#create the MCP4725 driver
dac=MCP4725(i2c,DEVICE_ADDRESS_1)

```

   
 

  



