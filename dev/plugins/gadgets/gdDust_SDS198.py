"""
Gadget Plugin for SDS198
Based on 
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetSerial import PluginGadgetSerial as GS
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdDust_SDS198'
PTYPE = PT_SENSOR
PNAME = 'Dust - SDS198'

UNIT = 'µg/m³'   #ANSI
#UNIT = 'ug/m3'   #ASCII

#######

class PluginGadget(GS):
    """ TODO """

    def __init__(self, module):
        super().__init__(module, 10)   # 10 byte data packet
        self.param = {
            # must be params
            'NAME':PNAME,
            'ENABLE':False,
            'TIMER':0,
            'PORT':'COM22',
            # instance specific params
            'RespVarPM100':'PM100',
            }

# -----

    def init(self):
        super().init()

        if self._ser:
            self._ser.init(9600, 8, None, 1) # baud=9600 databits=8 parity=none stopbits=1
            #self._ser.set_dtr(True)    # DTR-pin to +
            #self._ser.set_rts(False)   # RTS-pin to -
        Variable.set_meta(self.param['RespVarPM100'], UNIT, '{:.1f}')

        self.sum_pm100 = 0
        self.sum_count = 0

# -----

    def exit(self):
        super().exit()

# -----

    def idle(self):
        while self.process():
            if self.timer_period <= 1000:
                self.timer(False)

# -----

    def timer(self, prepare:bool):
        if self.sum_count:
            source = self.param['NAME']
            pm100 = self.sum_pm100 / self.sum_count
            print(pm100)

            key = self.param['RespVarPM100']
            Variable.set(key, pm100, source)

            self.sum_pm100 = 0
            self.sum_count = 0

# =====

    def is_valid(self):
        if self.data[0] != 0xAA:   # Head
            return False
        if self.data[9] != 0xAB:   # Tail
            return False
        if self.data[1] != 0xCF:   # Command ID
            return False
        sum = 0
        for i in range(2, 8):
            sum += self.data[i]
        if self.data[8] != (sum & 0xFF):    # Checksum
            return False
        return True

# -----

    def interpret(self):
        pm100 = (self.data[5] << 8) | self.data[4]

        self.sum_pm100 += pm100
        self.sum_count += 1

        self._remove_data(self.packet_size)
        return

#######
