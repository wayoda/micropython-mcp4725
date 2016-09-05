#Library for the MCP4725 I2C bus DAC 
from machine import I2C

#The MCP4725 has support from 2 addresses
BUS_ADDRESS = [0x62,0x63]

#The device supports a few power down modes on startup and during operation 
POWER_DOWN_MODE = {'Off':0, '1k':1, '100k':2, '500k':3}
        
class MCP4725:
    def __init__(self,i2c, address=BUS_ADDRESS[0]) :
        self.i2c=i2c
        self.address=address
        self._writeBuffer=bytearray(2)
        
    def write(self,value):
        if value < 0:
            value=0
        value=value & 0xFFF
        self._writeBuffer[0]=(value>>8) & 0xFF
        self._writeBuffer[1]=value & 0xFF
        return self.i2c.writeto(self.address,self._writeBuffer)==2

    def read(self):
        buf=bytearray(5)
        if self.i2c.readfrom_into(self.address,buf) ==5:
            eeprom_write_busy=(buf[0] & 0x80)==0
            power_down=self._powerDownKey((buf[0] >> 1) & 0x03)
            value=((buf[1]<<8) | (buf[2])) >> 4
            eeprom_power_down=self._powerDownKey((buf[3]>>5) & 0x03)
            eeprom_value=((buf[3] & 0x0f)<<8) | buf[4] 
            return (eeprom_write_busy,power_down,value,eeprom_power_down,eeprom_value)
        return None

    def config(self,power_down='Off',value=0,eeprom=False):
        buf=bytearray()
        conf=0x40 | (POWER_DOWN_MODE[power_down] << 1)
        if eeprom:
            #store the powerdown and output value in eeprom
            conf=conf | 0x60
        buf.append(conf)
        #check value range
        if value<0:
            value=0
        value=value & 0xFFF
        buf.append(value >> 4)
        buf.append((value & 0x0F)<<4)
        return self.i2c.writeto(self.address,buf)==3

    def _powerDownKey(self,value):
        for key,item in POWER_DOWN_MODE.items():
            if item == value:
                return key
                
 
