"""
@name: PyHouse/src/test/test_mixin.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jun 40, 2013
@summary: Test handling the information for a house.

"""

# Import system type stuff

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, PyHouseAPIs, \
            CoreServicesInformation, \
            ComputerInformation, \
            HouseInformation, HouseObjs, \
            TwistedInformation, \
            XmlInformation
from Modules.utils.tools import PrettyPrintAny


class SetupPyHouseObj(object):
    """
    """

    def BuildPyHouse(self):
        l_ret = PyHouseData()
        l_ret.APIs = PyHouseAPIs
        l_ret.Computer = ComputerInformation()
        l_ret.House = HouseInformation()
        l_ret.House.OBJs = HouseObjs()
        l_ret.Services = CoreServicesInformation()
        l_ret.Twisted = TwistedInformation()
        l_ret.Xml = XmlInformation()
        return l_ret


class Setup(SetupPyHouseObj):

    def __init__(self):
        self.m_pyhouse_obj = self.BuildPyHouse()
        print('test_mixin.Setup()')
        # PrettyPrintAny(self, 'test_mixin - Setup() - self')
        # PrettyPrintAny(self.m_pyhouse_obj, 'test_mixin - Setup() - pyhouse_obj')

# ## END DBK
