"""
@name:      PyHouse/src/Modules/Irrigation/test/test_irrigation_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 30, 2015
@summary:

Passed all 7 tests - DBK - 2016-08-20

"""

__updated__ = '2016-08-20'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Housing.Irrigation.irrigation_xml import Xml as irrigationXml
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = irrigationXml


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        self.assertEqual(self.m_pyhouse_obj.House.Irrigation, None)


class B1_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Zone(self):
        """
        """
        l_xml = self.m_xml.irrigation_zone
        l_obj = self.m_api._read_one_zone(l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-01-A - Zone'))
        self.assertEqual(l_obj.Name, 'Front Rotors # 1')

    def test_02_System(self):
        """
        """
        l_xml = self.m_xml.irrigation_system
        l_obj = self.m_api._read_one_irrigation_system(l_xml)
        self.assertEqual(l_obj.Name, 'LawnSystem')

    def test_03_Irrigation(self):
        """
        """
        l_xml = self.m_xml.irrigation_sect
        l_obj = self.m_api.read_irrigation_xml(self.m_pyhouse_obj)
        self.assertEqual(len(l_obj), 3)


class C1_Write(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Zone(self):
        """
        """
        l_irr = self.m_api.read_irrigation_xml(self.m_pyhouse_obj)
        l_sys = l_irr[0]
        l_obj = l_sys.Zones[0]
        l_xml = self.m_api._write_one_zone(l_obj)
        self.assertEqual(self.m_pyhouse_obj.House.Irrigation, None)

    def test_02_System(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        l_irr = self.m_api.read_irrigation_xml(self.m_pyhouse_obj)
        l_sys = l_irr[0]
        l_xml = self.m_api._write_one_system(l_sys)
        self.assertEqual(self.m_pyhouse_obj.House.Irrigation, None)

    def test_03_Irrigation(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        l_irr = self.m_api.read_irrigation_xml(self.m_pyhouse_obj)
        l_obj = self.m_api.write_irrigation_xml(l_irr)
        self.assertEqual(self.m_pyhouse_obj.House.Irrigation, None)

# ## END DBK
