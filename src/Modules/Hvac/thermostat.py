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
from Modules.Utilities import xml_tools
from Modules.Utilities import pyh_log
# from Modules.Utilities.tools import PrettyPrintAny

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.Thermostat  ')


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
        return p_obj

    def _read_family_data(self, p_obj, p_xml, p_pyhouse_obj):
        try:
            l_family = p_obj.ControllerFamily
            l_api = p_pyhouse_obj.House.OBJs.FamilyData[l_family].FamilyModuleAPI
            l_api.extract_device_xml(p_obj, p_xml)
        except KeyError as e_err:
            LOG.error('ReadFamilyData ERROR {0:}'.format(e_err))

    def read_one_thermostat_xml(self, p_thermostat_element, p_pyhouse_obj):
        """
        @return: a ThermostatData object
        """
        l_thermostat_obj = ThermostatData()
        self.read_base_object_xml(l_thermostat_obj, p_thermostat_element)
        l_thermostat_obj.Key = self.m_count  # Renumber
        self._read_thermostat_data(l_thermostat_obj, p_thermostat_element)
        self._read_family_data(l_thermostat_obj, p_thermostat_element, p_pyhouse_obj)
        return l_thermostat_obj

    def read_all_thermostats_xml(self, p_pyhouse_obj):
        """
        """
        l_xml_sect = self.setup_xml(p_pyhouse_obj)
        l_ret = {}
        self.m_count = 0
        if l_xml_sect == None:  # no thermostats defined
            return l_ret
        try:
            for l_xml in l_xml_sect.iterfind('Thermostat'):
                l_obj = self.read_one_thermostat_xml(l_xml, p_pyhouse_obj)
                l_ret[self.m_count] = l_obj
                self.m_count += 1
        except AttributeError as e_err:
            LOG.error('ReadAllThermostats AttributeError {0:}'.format(e_err))
        return l_ret

    def _write_thermostat_data(self, p_obj, p_xml):
        self.put_float_element(p_xml, 'CoolSetPoint', p_obj.CoolSetPoint)
        self.put_text_element(p_xml, 'ControllerFamily', p_obj.ControllerFamily)
        self.put_float_element(p_xml, 'CurrentTemperature', p_obj.CurrentTemperature)
        self.put_float_element(p_xml, 'HeatSetPoint', p_obj.HeatSetPoint)
        self.put_text_element(p_xml, 'ThermostatMode', p_obj.ThermostatMode)
        self.put_text_element(p_xml, 'ThermostatScale', p_obj.ThermostatScale)
        pass

    def _write_family_data(self, p_obj, p_xml, p_pyhouse_obj):
        try:
            l_api = p_pyhouse_obj.House.OBJs.FamilyData[p_obj.ControllerFamily].FamilyModuleAPI
            l_api.insert_device_xml(p_xml, p_obj)
        except KeyError as e_err:
            LOG.error('Write Family Key Error {0:}'.format(e_err))

    def write_one_thermostat_xml(self, p_thermostat_obj, p_pyhouse_obj):
        """
        """
        l_xml = self.write_base_object_xml('Thermostat', p_thermostat_obj)
        self._write_thermostat_data(p_thermostat_obj, l_xml)
        self._write_family_data(p_thermostat_obj, l_xml, p_pyhouse_obj)
        return l_xml

    def write_all_thermostats_xml(self, p_thermostat_sect_obj, p_pyhouse_obj):
        """Create a sub tree for 'Internet' - the sub elements do not have to be present.
        @return: a sub tree ready to be appended to "something"
        """
        l_xml = ET.Element('ThermostatSection')
        self.m_count = 0
        try:
            for l_obj in p_thermostat_sect_obj.itervalues():
                l_entry = self.write_one_thermostat_xml(l_obj, p_pyhouse_obj)
                l_xml.append(l_entry)
                self.m_count += 1
        except AttributeError as e:
            LOG.error('ERROR writing all thermostats {0:}'.format(e))
        return l_xml


class Utility(ReadWriteConfigXml):
    """
    """

    def update_pyhouse_obj(self, p_pyhouse_obj):
        p_pyhouse_obj.House.OBJs.Thermostats = ThermostatData()

    def add_api_references(self, p_pyhouse_obj):
        pass

    def setup_xml(self, p_pyhouse_obj):
        l_xml = p_pyhouse_obj.Xml.XmlRoot
        try:
            l_xml = l_xml.find('HouseDivision')
            l_xml = l_xml.find('ThermostatSection')
        except AttributeError as e_err:
            LOG.error('SetupXML ERROR {0:}'.format(e_err))
        return l_xml


class API(Utility):

    m_pyhouse_obj = None

    def __init__(self):
        if g_debug >= 1:
            LOG.info("Initialized.")

    def Start(self, p_pyhouse_obj):
        self.update_pyhouse_obj(p_pyhouse_obj)
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.House.OBJs.Thermostats = self.read_all_thermostats_xml(p_pyhouse_obj)
        LOG.info("Started.")

    def Stop(self):
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        l_xml = self.write_all_thermostats_xml(self.m_pyhouse_obj.House.OBJs.Thermostats, self.m_pyhouse_obj)
        p_xml.append(l_xml)
        LOG.info("Saved XML.")
        return l_xml

# ## END DBK
