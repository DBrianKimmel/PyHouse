"""
@name:      /home/briank/workspace/PyHouse/src/Modules/Families/Hue/_test/test_Hue_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Dec 18, 2017
@summary:   Test

Passed all 7 tests - DBK - 2018-02-13

"""
from Modules.Computer.Bridges.bridges_data import BridgesInformation

__updated__ = '2019-07-05'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from Modules.Core.data_objects import LightData, HouseInformation
from Modules.Families.Hue.Hue_xml import Xml as HueXml

from Modules.Core.Utilities.device_tools import XML as deviceXML
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """ Set up pyhouse object
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_device = LightData()
        self.m_version = '1.4.0'
        self.m_api = deviceXML


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_Hue_xml')


class A1_Prep(SetupMixin, unittest.TestCase):
    """ This section tests the setup
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_device = None

    def test_01_PyHouse(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        self.assertIsInstance(self.m_pyhouse_obj.House, HouseInformation)

    def test_02_FindXml(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.lighting_sect.tag, 'LightingSection')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection')
        self.assertEqual(self.m_xml.button_sect.tag, 'ButtonSection')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection')

    def test_03_Read(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_xml = self.m_xml.bridges_sect
        l_bridges = BridgesInformation()
        l_dict = HueXml.ReadXml(l_bridges, l_xml)
        pass

    def test_04_Objs(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        pass

    def test_05_XML(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        pass

    def test_06_Device(self):
        """ Be sure that the XML contains the right stuff.
        """

# ## END DBK
