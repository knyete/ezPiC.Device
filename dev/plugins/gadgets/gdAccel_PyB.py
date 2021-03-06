"""
Gadget Plugin for PyBoard-Accelerometer
"""
import pyb # will fail on none PyBoards

from com.Globals import *

import dev.Gadget as Gadget
import dev.Variable as Variable

#######

EZPID = 'gdPyBAccel'
PTYPE = PT_SENSOR
PNAME = 'Acc. - PyBoard-Accelerometer'

class PluginGadget(Gadget.PluginGadgetBase):

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            'NAME':'PyB-Accel', # must be params
            'ENABLE':False,
            'TIMER':1000,
            'name_x':'X', # instance specific params
            'name_y':'Y',
            'name_z':'Z',
            }

# -----

    def init(self):
        super().init()
        self._accel = pyb.Accel()

# -----

    def timer(self, prepare:bool):
        x, y, z = self._accel.x(), self._accel.y(), self._accel.z()

        Variable.set((self.param['NAME'], self.param['name_x']), x)
        Variable.set((self.param['NAME'], self.param['name_y']), y)
        Variable.set((self.param['NAME'], self.param['name_z']), z)
