"""
@name:      Modules/House/Family/insteon/_test/test_insteon_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2019 by D. Brian Kimmel
@note:      Created on Apr 1, 2011
@license:   MIT License
@summary:   This module tests Insteon_device

Passed all 1 tests - DBK - 2015-07-26
"""

__updated__ = '2019-08-19'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Family.insteon.insteon_data import InsteonData
from Modules.House.Family.insteon import insteon_device
from Modules.Core.Utilities.device_tools import XML as deviceXML

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_xml = SetupPyHouseObj().BuildXml()


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_Insteon_device')


class C01_API(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = insteon_device.API(self.m_pyhouse_obj)
        self.m_device = InsteonData()
        self.m_light = deviceXML().read_base_device_object_xml(self.m_device, self.m_xml.light)

    def test_01_Init(self):
        """ Be sure that the XML contains the right stuff.
        """
        pass

# def suite():
#    suite = unittest.TestSuite()
#    # suite.addTest(Test_02_API('test_0202_Init'))
#    return suite

# ## END
