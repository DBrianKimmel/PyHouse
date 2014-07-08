"""
@name: PyHouse/src/Modules/communication/test/test_send_email.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jun 3, 2014
@summary: Schedule events


"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ThermostatData
from Modules.hvac import thermostat
from Modules.housing import house
from Modules.web import web_utils
from Modules.Core import setup
from Modules.utils.tools import PrettyPrintAny
from src.test import xml_data


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = setup.build_pyhouse_obj(self)
        self.m_pyhouse_obj.Xml.XmlRoot = self.m_root_xml
        self.m_thermostat_obj = ThermostatData()
        self.m_api = thermostat.API()
        self.m_pyhouse_obj = house.API().update_pyhouse_obj(self.m_pyhouse_obj)
        PrettyPrintAny(self.m_pyhouse_obj, 'SetupMixin.Setup - PyHouse_obj', 100)
        return self.m_pyhouse_obj


class Test_02_XML(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        self.m_pyhouse_obj = SetupMixin.setUp(self)
        house.API().update_pyhouse_obj(self.m_pyhouse_obj)
        self.m_house_div_xml = self.m_root_xml.find('HouseDivision')
        self.m_thermostat_sect_xml = self.m_house_div_xml.find('ThermostatSection')
        self.m_thermostat_xml = self.m_thermostat_sect_xml.find('Thermostat')
        # PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse_obj', 120)

    def test_0201_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_house_div_xml.tag, 'HouseDivision', 'XML - No House Division')
        self.assertEqual(self.m_thermostat_sect_xml.tag, 'ThermostatSection', 'XML - No Thermostat section')
        self.assertEqual(self.m_thermostat_xml.tag, 'Thermostat', 'XML - No Thermostat Entry')
        # PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse_obj', 120)
        # PrettyPrintAny(self.m_pyhouse_obj.Xml, '201 PyHouse_obj.Xml', 120)



    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass


# ## END DBK
