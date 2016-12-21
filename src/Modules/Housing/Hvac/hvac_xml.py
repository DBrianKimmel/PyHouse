"""
-*- test-case-name: PyHouse.src.Modules.Hvac.test.test_hvac_xml -*-

@name:      PyHouse/src/Modules/Hvac/hvac_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 12, 2015
@Summary:

"""

__updated__ = '2016-11-08'

#  Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyMh files
from Modules.Core.data_objects import HvacData, ThermostatData, UuidData
from Modules.Families.family_utils import FamUtil
from Modules.Utilities.device_tools import XML as deviceXML
from Modules.Utilities.uuid_tools import Uuid as UtilUuid
from Modules.Utilities.xml_tools import PutGetXML
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Hvac_xml       ')


class Utility(object):

    @staticmethod
    def _read_base(p_pyhouse_obj, p_xml):
        l_obj = ThermostatData()
        deviceXML.read_base_device_object_xml(p_pyhouse_obj, l_obj, p_xml)
        return l_obj

    @staticmethod
    def _read_thermostat_base(p_pyhouse_obj, p_xml):
        l_obj = Utility._read_base(p_pyhouse_obj, p_xml)
        l_obj.DeviceType = 2
        l_obj.DeviceSubType = 1
        return l_obj

    @staticmethod
    def _read_thermostat_data(_p_pyhouse_obj, p_obj, p_xml):
        """
        @return: a ThermostatData object.
        """
        p_obj.CoolSetPoint = PutGetXML.get_float_from_xml(p_xml, 'CoolSetPoint', p_default=76.0)
        p_obj.HeatSetPoint = PutGetXML.get_float_from_xml(p_xml, 'HeatSetPoint', 68.0)
        p_obj.ThermostatMode = PutGetXML.get_text_from_xml(p_xml, 'ThermostatMode', 'Cool')
        p_obj.ThermostatScale = PutGetXML.get_text_from_xml(p_xml, 'ThermostatScale', 'F')
        #
        p_obj.CurrentTemperature = PutGetXML.get_float_from_xml(p_xml, 'CurrentTemperature')
        return p_obj

    @staticmethod
    def _read_family_data(p_pyhouse_obj, p_obj, p_xml):
        l_ret = FamUtil.read_family_data(p_pyhouse_obj, p_obj, p_xml)
        return l_ret

    @staticmethod
    def _read_one_thermostat_xml(p_pyhouse_obj, p_xml):
        """
        @return: a ThermostatData object
        """
        l_thermostat_obj = Utility._read_thermostat_base(p_pyhouse_obj, p_xml)
        Utility._read_thermostat_data(p_pyhouse_obj, l_thermostat_obj, p_xml)
        Utility._read_family_data(p_pyhouse_obj, l_thermostat_obj, p_xml)
        return l_thermostat_obj

    @staticmethod
    def _read_all_thermostats_xml(p_pyhouse_obj, p_xml):
        l_dict = {}
        l_count = 0
        try:
            for l_xml in p_xml.iterfind('Thermostat'):
                l_obj = Utility._read_one_thermostat_xml(p_pyhouse_obj, l_xml)
                l_obj.Key = l_count
                l_dict[l_count] = l_obj
                l_uuid_obj = UuidData()
                l_uuid_obj.UUID = l_obj.UUID
                l_uuid_obj.UuidType = 'Thermostat'
                UtilUuid.add_uuid(p_pyhouse_obj, l_uuid_obj)
                l_count += 1
        except AttributeError as e_err:
            LOG.error('Reading Hvac.Thermostat information - {}'.format(e_err))
        LOG.info("Loaded {} Thermostats".format(l_count))
        return l_dict

    @staticmethod
    def _write_thermostat_base(p_tag_name, p_obj):
        l_xml = deviceXML.write_base_device_object_xml(p_tag_name, p_obj)
        return l_xml

    @staticmethod
    def _write_thermostat_data(p_out_xml, p_obj):
        PutGetXML.put_float_element(p_out_xml, 'CoolSetPoint', p_obj.CoolSetPoint)
        PutGetXML.put_float_element(p_out_xml, 'HeatSetPoint', p_obj.HeatSetPoint)
        PutGetXML.put_text_element(p_out_xml, 'ThermostatMode', p_obj.ThermostatMode)
        PutGetXML.put_text_element(p_out_xml, 'ThermostatScale', p_obj.ThermostatScale)
        PutGetXML.put_float_element(p_out_xml, 'CurrentTemperature', p_obj.CurrentTemperature)
        return p_out_xml

    @staticmethod
    def _write_family_data(p_pyhouse_obj, p_obj, p_xml):
        try:
            l_api = p_pyhouse_obj.House.FamilyData[p_obj.DeviceFamily].FamilyXmlModuleAPI
            l_api.WriteXml(p_xml, p_obj)
        except (KeyError, AttributeError) as e_err:
            l_msg = 'Write Family Error {}  Family:{}'.format(e_err, p_obj.DeviceFamily)
            LOG.error(l_msg)

    @staticmethod
    def _write_one_thermostat_xml(p_pyhouse_obj, p_obj):
        l_xml = Utility._write_thermostat_base('Thermostat', p_obj)
        Utility._write_thermostat_data(l_xml, p_obj)
        Utility._write_family_data(p_pyhouse_obj, p_obj, l_xml)
        return l_xml

    @staticmethod
    def _write_all_thermostats_xml(p_pyhouse_obj):
        """Write the XML for all the thermostats.
        """
        l_count = 0
        l_thermostats = p_pyhouse_obj.House.Hvac.Thermostats
        l_xml = ET.Element('ThermostatSection')
        try:
            for l_obj in l_thermostats.itervalues():
                l_entry = Utility._write_one_thermostat_xml(p_pyhouse_obj, l_obj)
                l_xml.append(l_entry)
                l_count += 1
        except:
            pass
        LOG.info("Saved {} Thermostats".format(l_count))
        return l_xml


class XML(object):

    @staticmethod
    def read_hvac_xml(p_pyhouse_obj):
        l_obj = HvacData()
        try:
            l_xml = p_pyhouse_obj.Xml.XmlRoot.find('HouseDivision')
            l_xml = l_xml.find('HvacSection')
            l_xml = l_xml.find('ThermostatSection')
            l_obj.Thermostats = Utility._read_all_thermostats_xml(p_pyhouse_obj, l_xml)
        except AttributeError:
            pass
        return l_obj

    @staticmethod
    def write_hvac_xml(p_pyhouse_obj, _p_xml):
        """Create a v1.4 tree for HVAC
        @param p_pyhouse_obj: is the mother data store
        @return: a sub tree ready to be appended to an element.
        """
        l_xml = ET.Element('HvacSection')  # HvacSection
        l_xml.append(Utility._write_all_thermostats_xml(p_pyhouse_obj))
        return l_xml

#  ## END DBK
