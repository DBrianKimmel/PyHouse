"""
@name:      PyHouse/src/Modules/Hvac/hvac_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 12, 2015
@Summary:

"""


# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Core.data_objects import ThermostatData
from Modules.Families.family_utils import FamUtil
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities.xml_tools import PutGetXML, XmlConfigTools

LOG = Logger.getLogger('PyHouse.Hvac_xml       ')
DIVISION = 'HouseDivision'
H_SECTION = 'HvacSection'
T_SECTION = 'ThermostatSection'
T_DEVICE = 'Thermostat'


class ThermostatXML(object):
    """
    """
    m_count = 0

    @staticmethod
    def _read_thermostat_base(p_thermostat_element):
        l_obj = ThermostatData()
        XmlConfigTools.read_base_object_xml(l_obj, p_thermostat_element)
        l_obj.DeviceType = 2
        return l_obj

    @staticmethod
    def _read_thermostat_data(p_obj, p_xml):
        """
        @return: a ThermostatData object.
        """
        p_obj.DeviceFamily = PutGetXML.get_text_from_xml(p_xml, 'DeviceFamily')
        p_obj.CoolSetPoint = PutGetXML.get_float_from_xml(p_xml, 'CoolSetPoint', 76.0)
        p_obj.CurrentTemperature = PutGetXML.get_float_from_xml(p_xml, 'CurrentTemperature')
        p_obj.HeatSetPoint = PutGetXML.get_float_from_xml(p_xml, 'HeatSetPoint', 68.0)
        p_obj.ThermostatMode = PutGetXML.get_text_from_xml(p_xml, 'ThermostatMode', 'Cool')
        p_obj.ThermostatScale = PutGetXML.get_text_from_xml(p_xml, 'ThermostatScale', 'F')
        return p_obj

    @staticmethod
    def _read_family_data(p_pyhouse_obj, p_obj, p_xml):
        l_ret = FamUtil.read_family_data(p_pyhouse_obj, p_obj, p_xml)
        return l_ret

    @staticmethod
    def _read_one_thermostat_xml(p_pyhouse_obj, p_thermostat_element):
        """
        @return: a ThermostatData object
        """
        l_thermostat_obj = ThermostatXML._read_thermostat_base(p_thermostat_element)
        ThermostatXML._read_thermostat_data(l_thermostat_obj, p_thermostat_element)
        ThermostatXML._read_family_data(p_pyhouse_obj, l_thermostat_obj, p_thermostat_element)
        return l_thermostat_obj

    def read_all_thermostats_xml(self, p_pyhouse_obj):
        """
        """
        try:
            l_section = p_pyhouse_obj.Xml.XmlRoot.find(DIVISION).find(H_SECTION)
        except AttributeError as e_err:
            LOG.error('Reading irrigation information - {}'.format(e_err))
            l_section = None
        l_obj = {}
        l_count = 0
        try:
            for l_xml in l_section.iterfind('abcd'):
                l_system = self._read_one_irrigation_system(l_xml)
                l_obj[l_count] = l_system
                l_count += 1
        except AttributeError as e_err:
            LOG.error('irrigationSystem: {}'.format(e_err))
        return l_obj

        l_xml_sect = p_pyhouse_obj.Xml.XmlRoot.find(DIVISION)
        l_ret = {}
        self.m_count = 0
        try:
            for l_xml in l_xml_sect.iterfind('Thermostat'):
                l_obj = ThermostatXML._read_one_thermostat_xml(p_pyhouse_obj, l_xml)
                l_ret[self.m_count] = l_obj
                self.m_count += 1
        except AttributeError as e_err:
            l_msg = 'ReadAllThermostats AttributeError {0:}'.format(e_err)
            LOG.error(l_msg)
        LOG.info("Loaded {} Thermostats".format(self.m_count))
        return l_ret


    def _write_thermostat_base(self, p_thermostat_obj):
        l_xml = XmlConfigTools().write_base_object_xml('Thermostat', p_thermostat_obj)
        return l_xml

    def _write_thermostat_data(self, p_out_xml, p_obj):
        PutGetXML.put_float_element(p_out_xml, 'CoolSetPoint', p_obj.CoolSetPoint)
        PutGetXML.put_text_element(p_out_xml, 'DeviceFamily', p_obj.DeviceFamily)
        PutGetXML.put_float_element(p_out_xml, 'CurrentTemperature', p_obj.CurrentTemperature)
        PutGetXML.put_float_element(p_out_xml, 'HeatSetPoint', p_obj.HeatSetPoint)
        PutGetXML.put_text_element(p_out_xml, 'ThermostatMode', p_obj.ThermostatMode)
        PutGetXML.put_text_element(p_out_xml, 'ThermostatScale', p_obj.ThermostatScale)
        return p_out_xml

    def _write_thermostat_family(self, p_pyhouse_obj, p_out_xml, p_obj):
        try:
            l_api = p_pyhouse_obj.House.RefOBJs.FamilyData[p_obj.DeviceFamily].FamilyModuleAPI
            l_api.WriteXml(p_out_xml, p_obj)
        except (KeyError, AttributeError) as e_err:
            l_msg = 'Write Family Error {}  Family:{}'.format(e_err, p_obj.DeviceFamily)
            LOG.error(l_msg)

    def _write_one_thermostat_xml(self, p_pyhouse_obj, p_thermostat_obj):
        l_out_xml = self._write_thermostat_base(p_thermostat_obj)
        self._write_thermostat_data(l_out_xml, p_thermostat_obj)
        self._write_thermostat_family(p_pyhouse_obj, l_out_xml, p_thermostat_obj)
        return l_out_xml

    def write_all_thermostats_xml(self, p_pyhouse_obj):
        """Create a v1.4 tree for HVAC
        @param p_pyhouse_obj: is the mother data store
        @return: a sub tree ready to be appended to an element.
        """
        l_xml = ET.Element(H_SECTION)  # HvacSection
        ET.SubElement(l_xml, T_SECTION)  # ThermostatSection
        l_count = 0
        try:
            for l_obj in p_pyhouse_obj.House.DeviceOBJs.Thermostats.itervalues():
                l_entry = self._write_one_thermostat_xml(p_pyhouse_obj, l_obj)
                l_xml.append(l_entry)
                l_count += 1
        except AttributeError as e_err:
            l_msg = 'ERROR writing all thermostats {0:}'.format(e_err)
            LOG.error(l_msg)
        return l_xml


class XML(object):
    """
    """

    def read_hvac_xml(self):
        pass

    def write_hvac_xml(self):
        pass

# ## END DBK
