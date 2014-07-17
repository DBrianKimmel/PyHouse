"""
@name: PyHouse/src/Modules/utils/test/test_config_file.py
@author: briank
@contact: <d.briankimmel@gmail.com>
@Copyright: (c)  2014 by briank
@license: MIT License
@note: Created on Jul 15, 2014
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ThermostatData
from Modules.utils import config_file
from Modules.housing import house
from Modules.Core import setup
# from Modules.utils.tools import PrettyPrintAny
from test import xml_data
from Modules.utils.tools import PrettyPrint, PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = setup.build_pyhouse_obj(self)
        self.m_pyhouse_obj.Xml.XmlRoot = self.m_root_xml
        self.m_thermostat_obj = ThermostatData()
        self.m_api = config_file.ConfigAPI()
        self.m_pyhouse_obj = house.API().update_pyhouse_obj(self.m_pyhouse_obj)
        # PrettyPrintAny(self.m_pyhouse_obj, 'SetupMixin.Setup - PyHouse_obj', 100)
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


    def test_0201_FindDir(self):
        l_dir = self.m_api._locate_config_dir()
        print(l_dir)

    def test_0202_FindFile(self):
        l_file = self.m_api._locate_config_file()
        print(l_file)

    def test_0221_ReadConfig(self):
        self.m_api.read_config_file(self.m_pyhouse_obj)
        PrettyPrintAny(self.m_pyhouse_obj.Xml, 'Xml', 120)
        PrettyPrintAny(self.m_pyhouse_obj.Xml.XmlRoot, 'XmlRoot', 120)

    def test_0231_WriteConfig(self):
        self.m_api.read_config_file(self.m_pyhouse_obj)
        l_xml = self.m_pyhouse_obj.Xml.XmlRoot
        l_file = self.m_pyhouse_obj.Xml.XmlFileName
        self.m_api.write_config_file(self.m_pyhouse_obj, l_xml, l_file)
        pass

# ## END DBK
