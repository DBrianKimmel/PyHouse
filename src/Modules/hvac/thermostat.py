"""
-*- test-case-name: PyHouse.src.Modules.hvac.test.test_thermostat -*-

@name: PyHouse/src/Modules/hvac/thermostat.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Mar 27, 2013
@summary: This module is for testing local node data.

Created on Mar 27, 2013

@author: briank
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Core.data_objects import ThermostatData
from Modules.utils import xml_tools
from Modules.utils import pyh_log
from Modules.utils.tools import PrettyPrintAny

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.Thermostat  >>')


class ReadWriteConfigXml(xml_tools.XmlConfigTools):
    """
    """
    m_count = 0

    def _read_thermostat_data(self, p_obj, p_xml):
        """
        @return: a ThermostatData object.
        """
        p_obj.CoolSetPoint = self.get_float_from_xml(p_xml, 'CoolSetPoint', 76.0)
        p_obj.ControllerFamily = self.get_text_from_xml(p_xml, 'ControllerFamily')
        p_obj.CurrentTemperature = self.get_float_from_xml(p_xml, 'CurrentTemperature')
        p_obj.HeatSetPoint = self.get_float_from_xml(p_xml, 'HeatSetPoint', 68.0)
        p_obj.ThermostatMode = self.get_text_from_xml(p_xml, 'ThermostatMode', 'Cool')
        p_obj.ThermostatScale = self.get_text_from_xml(p_xml, 'ThermostatScale', 'F')

    def _read_family_data(self, p_obj, p_xml):
        l_family = p_obj.ControllerFamily
        l_api = self.m_pyhouse_obj.House.OBJs.FamilyData[l_family].ModuleAPI
        l_api.extract_device_xml(p_obj, p_xml)

    def read_one_thermostat_xml(self, p_thermostat_element):
        """
        @return: a ThermostatData object
        """
        l_thermostat_obj = ThermostatData()
        self.read_base_object_xml(l_thermostat_obj, p_thermostat_element)
        l_thermostat_obj.Key = self.m_count  # Renumber
        self._read_thermostat_data(l_thermostat_obj, p_thermostat_element)
        self._read_family_data(l_thermostat_obj, p_thermostat_element)
        return l_thermostat_obj

    def read_all_thermostats_xml(self, p_thermostat_sect_element):
        """
        """
        l_ret = {}
        self.m_count = 0
        for l_xml in p_thermostat_sect_element.iterfind('Thermostat'):
            l_obj = self.read_one_thermostat_xml(l_xml)
            l_ret[self.m_count] = l_obj
            self.m_count += 1
        return l_ret

    def _write_thermostat_data(self, p_obj, p_xml):
        self.put_float_element(p_xml, 'CoolSetPoint', p_obj.CoolSetPoint)
        self.put_text_element(p_xml, 'ControllerFamily', p_obj.ControllerFamily)
        self.put_float_element(p_xml, 'CurrentTemperature', p_obj.CurrentTemperature)
        self.put_float_element(p_xml, 'HeatSetPoint', p_obj.HeatSetPoint)
        self.put_text_element(p_xml, 'ThermostatMode', p_obj.ThermostatMode)
        self.put_text_element(p_xml, 'ThermostatScale', p_obj.ThermostatScale)
        pass

    def _write_family_data(self, p_obj, p_xml):
        l_api = self.m_pyhouse_obj.House.OBJs.FamilyData[p_obj.ControllerFamily].ModuleAPI
        l_api.insert_device_xml(p_xml, p_obj)

    def write_one_thermostat_xml(self, p_thermostat_obj):
        """
        """
        l_xml = self.write_base_object_xml('Thermostat', p_thermostat_obj)
        self._write_thermostat_data(p_thermostat_obj, l_xml)
        self._write_family_data(p_thermostat_obj, l_xml)
        return l_xml

    def write_all_thermostats_xml(self, p_thermostat_sect_obj):
        """Create a sub tree for 'Internet' - the sub elements do not have to be present.
        @return: a sub tree ready to be appended to "something"
        """
        l_xml = ET.Element('ThermostatSection')
        self.m_count = 0
        for l_obj in p_thermostat_sect_obj.itervalues():
            l_entry = self.write_one_thermostat_xml(l_obj)
            l_xml.append(l_entry)
            self.m_count += 1
        return l_xml


class API(ReadWriteConfigXml):

    m_pyhouse_obj = None

    def __init__(self):
        LOG.info("Initialized.")

    def Start(self, p_pyhouse_obj):
        LOG.info("Starting.")
        l_xml = p_pyhouse_obj.Xml.XmlRoot
        print(l_xml)
        l_xml = l_xml.find('HouseDivision')
        # PrettyPrintAny(l_xml, 'Thermostat - Start - HouseDivision', 100)
        l_xml = l_xml.find('ThermostatSection')
        print(l_xml)
        p_pyhouse_obj.House.OBJs.Thermostats = ThermostatData()
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.House.OBJs.Thermostats = self.read_all_thermostats_xml(l_xml)
        # PrettyPrintAny(p_pyhouse_obj, 'Thermostat - start - pyhouse', 100)
        # PrettyPrintAny(p_pyhouse_obj.House, 'Thermostat - start - pyhouse.House', 100)
        # PrettyPrintAny(p_pyhouse_obj.House.OBJs, 'Thermostat - start - pyhouse.House.OBJs', 100)
        LOG.info("Started.")

    def Stop(self, p_xml):
        l_xml = self.write_all_thermostats_xml(self.m_pyhouse_obj)
        p_xml.append(l_xml)
        LOG.info("Stopped.")
        return l_xml

# ## END DBK
