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
from Modules.Core.data_objects import PyHouseData, ComputerData, CoreServicesData, HouseData, TwistedInfo, XmlData
from Modules.utils.tools import PrettyPrintAny


class SetupPyHouseObj(object):
    """
    """

    def BuildPyHouse(self):
        l_ret = PyHouseData()
        l_ret.Computer = ComputerData()
        l_ret.House = HouseData()
        l_ret.Services = CoreServicesData()
        l_ret.Twisted = TwistedInfo()
        l_ret.Xml = XmlData()
        return l_ret


class Setup(SetupPyHouseObj):

    def __init__(self):
        self.m_pyhouse_obj = self.BuildPyHouse()
        print('test_mixin.Setup()')
        PrettyPrintAny(self, 'test_mixin - self')

# ## END DBK
