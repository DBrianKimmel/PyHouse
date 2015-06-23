"""
-*- test-case-name: PyHouse.src.Modules.Hvac.test.test_thermostat -*-

@name:      PyHouse/src/Modules/Hvac/thermostats.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 27, 2013
@summary:   This module is for testing local node data.

"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Core.data_objects import ThermostatData
from Modules.Utilities import xml_tools
from Modules.Families.family_utils import FamUtil
from Modules.Computer import logging_pyh as Logger

g_debug = 0
LOG = Logger.getLogger('PyHouse.Thermostat     ')



class ReadWriteConfigXml(xml_tools.XmlConfigTools):
    """
    """
    m_count = 0

    def _read_thermostat_base(self, p_thermostat_element):
        l_obj = ThermostatData()
        self.read_base_object_xml(l_obj, p_thermostat_element)
        l_obj.Key = self.m_count  # Renumber
        l_obj.DeviceType = 2
        return l_obj

    def _read_thermostat_data(self, p_obj, p_xml):
        """
        @return: a ThermostatData object.
        """
        p_obj.ControllerFamily = self.get_text_from_xml(p_xml, 'ControllerFamily')
        p_obj.CoolSetPoint = self.get_float_from_xml(p_xml, 'CoolSetPoint', 76.0)
        p_obj.CurrentTemperature = self.get_float_from_xml(p_xml, 'CurrentTemperature')
        p_obj.HeatSetPoint = self.get_float_from_xml(p_xml, 'HeatSetPoint', 68.0)
        p_obj.ThermostatMode = self.get_text_from_xml(p_xml, 'ThermostatMode', 'Cool')
        p_obj.ThermostatScale = self.get_text_from_xml(p_xml, 'ThermostatScale', 'F')
        return p_obj

    def _read_family_data(self, p_pyhouse_obj, p_obj, p_xml):
        l_ret = FamUtil.read_family_data(p_pyhouse_obj, p_obj, p_xml)
        return l_ret

    def _read_one_thermostat_xml(self, p_pyhouse_obj, p_thermostat_element):
        """
        @return: a ThermostatData object
        """
        l_thermostat_obj = self._read_thermostat_base(p_thermostat_element)
        self._read_thermostat_data(l_thermostat_obj, p_thermostat_element)
        self._read_family_data(p_pyhouse_obj, l_thermostat_obj, p_thermostat_element)
        return l_thermostat_obj

    def read_all_thermostats_xml(self, p_pyhouse_obj):
        """
        """
        l_xml_sect = self.setup_xml(p_pyhouse_obj)
        l_ret = {}
        self.m_count = 0
        try:
            for l_xml in l_xml_sect.iterfind('Thermostat'):
                l_obj = self._read_one_thermostat_xml(p_pyhouse_obj, l_xml)
                l_ret[self.m_count] = l_obj
                self.m_count += 1
        except AttributeError as e_err:
            l_msg = 'ReadAllThermostats AttributeError {0:}'.format(e_err)
            LOG.error(l_msg)
        return l_ret


    def _write_thermostat_base(self, p_thermostat_obj):
        l_xml = self.write_base_object_xml('Thermostat', p_thermostat_obj)
        return l_xml

    def _write_thermostat_data(self, p_out_xml, p_obj):
        self.put_float_element(p_out_xml, 'CoolSetPoint', p_obj.CoolSetPoint)
        self.put_text_element(p_out_xml, 'ControllerFamily', p_obj.ControllerFamily)
        self.put_float_element(p_out_xml, 'CurrentTemperature', p_obj.CurrentTemperature)
        self.put_float_element(p_out_xml, 'HeatSetPoint', p_obj.HeatSetPoint)
        self.put_text_element(p_out_xml, 'ThermostatMode', p_obj.ThermostatMode)
        self.put_text_element(p_out_xml, 'ThermostatScale', p_obj.ThermostatScale)
        return p_out_xml

    def _write_thermostat_family(self, p_pyhouse_obj, p_out_xml, p_obj):
        try:
            l_api = p_pyhouse_obj.House.RefOBJs.FamilyData[p_obj.ControllerFamily].FamilyModuleAPI
            l_api.WriteXml(p_out_xml, p_obj)
        except (KeyError, AttributeError) as e_err:
            l_msg = 'Write Family Error {}  Family:{}'.format(e_err, p_obj.ControllerFamily)
            LOG.error(l_msg)

    def _write_one_thermostat_xml(self, p_pyhouse_obj, p_thermostat_obj):
        l_out_xml = self._write_thermostat_base(p_thermostat_obj)
        self._write_thermostat_data(l_out_xml, p_thermostat_obj)
        self._write_thermostat_family(p_pyhouse_obj, l_out_xml, p_thermostat_obj)
        return l_out_xml

    def write_all_thermostats_xml(self, p_pyhouse_obj):
        """Create a sub tree for 'Internet' - the sub elements do not have to be present.
        @return: a sub tree ready to be appended to "something"
        """
        l_xml = ET.Element('ThermostatSection')
        self.m_count = 0
        try:
            for l_obj in p_pyhouse_obj.House.DeviceOBJs.Thermostats.itervalues():
                l_entry = self._write_one_thermostat_xml(p_pyhouse_obj, l_obj)
                l_xml.append(l_entry)
                self.m_count += 1
        except AttributeError as e_err:
            l_msg = 'ERROR writing all thermostats {0:}'.format(e_err)
            LOG.error(l_msg)
            print(l_msg)
        return l_xml


class Utility(ReadWriteConfigXml):
    """
    """

    def update_pyhouse_obj(self, p_pyhouse_obj):
        p_pyhouse_obj.House.DeviceOBJs.Thermostats = ThermostatData()

    def add_api_references(self, p_pyhouse_obj):
        pass

    def setup_xml(self, p_pyhouse_obj):
        try:
            l_xml = p_pyhouse_obj.Xml.XmlRoot.find('HouseDivision').find('ThermostatSection')
        except AttributeError as e_err:
            LOG.error('SetupXML ERROR {0:}'.format(e_err))
            l_xml = None
        return l_xml


class API(Utility):

    m_pyhouse_obj = None

    def __init__(self):
        if g_debug >= 1:
            LOG.info("Initialized.")

    def Start(self, p_pyhouse_obj):
        self.update_pyhouse_obj(p_pyhouse_obj)
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.House.DeviceOBJs.Thermostats = self.read_all_thermostats_xml(p_pyhouse_obj)
        LOG.info("Started.")

    def Stop(self):
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        l_xml = self.write_all_thermostats_xml(self.m_pyhouse_obj)
        p_xml.append(l_xml)
        LOG.info("Saved XML.")
        return l_xml

# ## END DBK
