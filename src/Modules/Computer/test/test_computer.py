"""
@name: C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/Computer/test/test_computer.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com>
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jul 25, 2014
@Summary:

"""

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, CoreServicesInformation
from Modules.Computer import computer
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = computer.API()


class Test_01_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def tearDown(self):
        pass

    def test_0101_Update(self):
        self.m_api.update_pyhouse_obj(self.m_pyhouse_obj)
        PrettyPrintAny(self.m_pyhouse_obj.Computer, 'PyHouse')

# ## END DBK
