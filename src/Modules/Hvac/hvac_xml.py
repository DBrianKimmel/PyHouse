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
from Modules.Utilities.device_tools import XML as deviceXML
from Modules.Utilities.xml_tools import PutGetXML
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Hvac_xml       ')


class Utility(object):

    @staticmethod
    def _read_thermostat_base(p_xml):
        l_obj = ThermostatData()
        deviceXML.read_base_device_object_xml(l_obj, p_xml)
        l_obj.DeviceType = 2
        l_obj.DeviceSubType = 73
        return l_obj

    @staticmethod
    def _write_thermostat_base(p_tag_name, p_obj):
        l_xml = deviceXML.write_base_device_object_xml(p_tag_name, p_obj)
        return l_xml


    @staticmethod
    def _read_thermostat_data(p_obj, p_xml):
        """
        @return: a ThermostatData object.
        """
        p_obj.CoolSetPoint = PutGetXML.get_float_from_xml(p_xml, 'CoolSetPoint', 76.0)
        p_obj.HeatSetPoint = PutGetXML.get_float_from_xml(p_xml, 'HeatSetPoint', 68.0)
        p_obj.ThermostatMode = PutGetXML.get_text_from_xml(p_xml, 'ThermostatMode', 'Cool')
        p_obj.ThermostatScale = PutGetXML.get_text_from_xml(p_xml, 'ThermostatScale', 'F')
        #
        p_obj.CurrentTemperature = PutGetXML.get_float_from_xml(p_xml, 'CurrentTemperature')
        return p_obj

    @staticmethod
    def _write_thermostat_data(p_out_xml, p_obj):
        PutGetXML.put_float_element(p_out_xml, 'CoolSetPoint', p_obj.CoolSetPoint)
        PutGetXML.put_float_element(p_out_xml, 'HeatSetPoint', p_obj.HeatSetPoint)
        PutGetXML.put_text_element(p_out_xml, 'ThermostatMode', p_obj.ThermostatMode)
        PutGetXML.put_text_element(p_out_xml, 'ThermostatScale', p_obj.ThermostatScale)
        PutGetXML.put_float_element(p_out_xml, 'CurrentTemperature', p_obj.CurrentTemperature)
        return p_out_xml


    @staticmethod
    def _read_family_data(p_pyhouse_obj, p_obj, p_xml):
        l_ret = FamUtil.read_family_data(p_pyhouse_obj, p_obj, p_xml)
        return l_ret

    @staticmethod
    def _write_family_data(p_pyhouse_obj, p_obj, p_xml):
        try:
            l_api = p_pyhouse_obj.House.FamilyData[p_obj.DeviceFamily].FamilyXmlModuleAPI
            l_api.WriteXml(p_xml, p_obj)
        except (KeyError, AttributeError) as e_err:
            l_msg = 'Write Family Error {}  Family:{}'.format(e_err, p_obj.DeviceFamily)
            LOG.error(l_msg)


    @staticmethod
    def _read_one_thermostat_xml(p_pyhouse_obj, p_xml):
        """
        @return: a ThermostatData object
        """
        l_thermostat_obj = Utility._read_thermostat_base(p_xml)
        Utility._read_thermostat_data(l_thermostat_obj, p_xml)
        Utility._read_family_data(p_pyhouse_obj, l_thermostat_obj, p_xml)
        return l_thermostat_obj

    @staticmethod
    def _write_one_thermostat_xml(p_pyhouse_obj, p_obj):
        l_xml = Utility._write_thermostat_base('Thermostat', p_obj)
        Utility._write_thermostat_data(l_xml, p_obj)
        Utility._write_family_data(p_pyhouse_obj, p_obj, l_xml)
        return l_xml


class XML(object):

    @staticmethod
    def read_hvac_xml(p_pyhouse_obj):
        l_obj = {}
        l_count = 0
        try:
            l_division = p_pyhouse_obj.Xml.XmlRoot.find('HouseDivision')
            # print(l_division.tag)
            l_h_section = l_division.find('HvacSection')
            # print(l_h_section.tag)
            # if l_section == None:
            l_section = l_h_section.find('ThermostatSection')
            # print(l_section.tag)
        except AttributeError as e_err:
            LOG.error('Reading Hvac information - {}'.format(e_err))
            l_section = None
        try:
            for l_xml in l_section.iterfind('Thermostat'):
                # print(l_xml.tag)
                l_therm = Utility._read_one_thermostat_xml(p_pyhouse_obj, l_xml)
                l_obj[l_count] = l_therm
                l_count += 1
        except AttributeError as e_err:
            # LOG.error('ERROR {}'.format(e_err))
            pass
        LOG.info("Loaded {} Thermostats".format(l_count))
        return l_obj

    @staticmethod
    def write_hvac_xml(p_pyhouse_obj, p_xml):
        """Create a v1.4 tree for HVAC
        @param p_pyhouse_obj: is the mother data store
        @return: a sub tree ready to be appended to an element.
        """
        l_xml = ET.Element('HvacSection')  # HvacSection
        ET.SubElement(l_xml, 'ThermostatSection')  # ThermostatSection
        l_count = 0
        try:
            for l_obj in p_pyhouse_obj.House.Hvac.itervalues():
                l_entry = Utility._write_one_thermostat_xml(p_pyhouse_obj, l_obj)
                l_xml.append(l_entry)
                l_count += 1
        except AttributeError as e_err:
            # l_msg = 'ERROR writing all thermostats {}'.format(e_err)
            # LOG.error(l_msg)
            pass
        LOG.info("Saved {} Thermostats".format(l_count))
        return l_xml

# ## END DBK
