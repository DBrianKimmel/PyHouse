"""
@name: PyHouse/src/Modules/families/Insteon/test/test_Insteon_device.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2011-2014 by D. Brian Kimmel
@note: Created on Apr 1, 2011
@license: MIT License
@summary: This module tests Insteon_device

Passed all 4 tests - DBK - 2014-07-18
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Families.Insteon.Insteon_data import InsteonData
from Modules.Families.Insteon import Insteon_device
from Modules.Core import conversions
from Modules.Lighting import lighting_lights
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_02_API(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = Insteon_device.API()
        self.m_controller_obj = InsteonData()

    def test_0202_Init(self):
        """ Be sure that the XML contains the right stuff.
        """
        pass

def suite():
    suite = unittest.TestSuite()
    suite.addTest(Test_02_API('test_0202_Init'))
    return suite

# ## END
