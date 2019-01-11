"""
@name:      PyHouse/src/Modules/families/Insteon/test/test_Insteon_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2019 by D. Brian Kimmel
@note:      Created on Apr 1, 2011
@license:   MIT License
@summary:   This module tests Insteon_device

Passed all 1 tests - DBK - 2015-07-26
"""

__updated__ = '2019-01-09'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Families.Insteon.Insteon_data import InsteonData
from Modules.Families.Insteon import Insteon_device
from Modules.Families.Insteon.Insteon_xml import Xml as insteonXml
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities.device_tools import XML as deviceXML


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_Insteon_device')


class C01_API(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = Insteon_device.API(self.m_pyhouse_obj)
        self.m_device = InsteonData()
        self.m_light = deviceXML().read_base_device_object_xml(self.m_pyhouse_obj, self.m_device, self.m_xml.light)
        insteonXml.ReadXml(self.m_light, self.m_xml.light)

    def test_01_Init(self):
        """ Be sure that the XML contains the right stuff.
        """
        pass


def suite():
    suite = unittest.TestSuite()
    # suite.addTest(Test_02_API('test_0202_Init'))
    return suite

# ## END
