"""
-*- test-case-name: /home/briank/PyHouse/src/Modules/Housing/Lighting/lighting_garagedoor.py -*-

@name:      /home/briank/PyHouse/src/Modules/Housing/Lighting/lighting_garagedoor.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2016 by D. Brian Kimmel
@note:      Created on Oct 5, 2016
@license:   MIT License
@summary:

"""

__updated__ = '2016-10-10'

#  Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyHouse files
from Modules.Computer import logging_pyh as Logging
from Modules.Core.data_objects import LightData, UuidData
from Modules.Families.family_utils import FamUtil
from Modules.Utilities.device_tools import XML as deviceXML
from Modules.Utilities.xml_tools import PutGetXML
from Modules.Utilities.uuid_tools import Uuid as UtilUuid

LOG = Logging.getLogger('PyHouse.LightingLights ')


class Utility(object):

    @staticmethod
    def _read_base_device(p_pyhouse_obj, p_xml):
        """
        @param p_xml: is the XML Element for the entire device
        @return: a Light data object with the base info filled in
        """
        l_obj = LightData()
        l_obj = deviceXML.read_base_device_object_xml(p_pyhouse_obj, l_obj, p_xml)
        l_obj.DeviceType = 1
        l_obj.DeviceSubType = 4
        return l_obj

    @staticmethod
    def _write_base_device(_p_pyhouse_obj, p_light_obj):
        l_xml = deviceXML.write_base_device_object_xml('Light', p_light_obj)
        return l_xml

    @staticmethod
    def _read_dooe_data(_p_pyhouse_obj, p_obj, p_xml):
        p_obj.CurLevel = PutGetXML.get_int_from_xml(p_xml, 'CurLevel', 0)
        p_obj.IsDimmable = PutGetXML.get_bool_from_xml(p_xml, 'IsDimmable', False)
        return p_obj  # for testing

    @staticmethod
    def _write_door_data(p_obj, p_xml):
        PutGetXML.put_text_element(p_xml, 'CurLevel', p_obj.CurLevel)
        PutGetXML.put_text_element(p_xml, 'IsDimmable', p_obj.IsDimmable)
        return p_xml

    @staticmethod
    def _read_family_data(p_pyhouse_obj, p_obj, p_xml):
        l_api = FamUtil.read_family_data(p_pyhouse_obj, p_obj, p_xml)
        return l_api  # for testing

    @staticmethod
    def _write_family_data(p_pyhouse_obj, p_obj, p_xml):
        try:
            l_family = p_obj.DeviceFamily
            l_family_obj = p_pyhouse_obj.House.FamilyData[l_family]
            l_api = l_family_obj.FamilyXmlModuleAPI
            l_api.WriteXml(p_xml, p_obj)
        except Exception as e_err:
            LOG.error('ERROR - {}'.format(e_err))

    @staticmethod
    def _read_one_door_xml(p_pyhouse_obj, p_xml):
        """
        Load all the xml for one controller.
        Base Device, Light, Family
        """
        try:
            l_obj = Utility._read_base_device(p_pyhouse_obj, p_xml)
            Utility._read_light_data(p_pyhouse_obj, l_obj, p_xml)
            Utility._read_family_data(p_pyhouse_obj, l_obj, p_xml)
        except Exception as e_err:
            LOG.error('ERROR - ReadOneController - {}'.format(e_err))
            l_obj = LightData()
        return l_obj

    @staticmethod
    def _write_one_door_xml(p_pyhouse_obj, p_controller_obj):
        l_xml = Utility._write_base_device(p_pyhouse_obj, p_controller_obj)
        Utility._write_light_data(p_controller_obj, l_xml)
        Utility._write_family_data(p_pyhouse_obj, p_controller_obj, l_xml)
        return l_xml


class API(object):

    @staticmethod
    def read_all_GarageDoors_xml(p_pyhouse_obj, p_light_sect_xml):
        """
        @param p_pyhouse_obj: is the master information store
        @param p_light_sect_xml: the "LightSection" of the config
        @param p_version: is the XML version of the file to use.
        @return: a dict of lights info
        """
        l_count = 0
        l_dict = {}
        try:
            for l_xml in p_light_sect_xml.iterfind('Light'):
                l_obj = Utility.read_one_door_xml(p_pyhouse_obj, l_xml)
                l_obj.Key = l_count  # Renumber
                l_dict[l_count] = l_obj
                l_uuid_obj = UuidData()
                l_uuid_obj.UUID = l_obj.UUID
                l_uuid_obj.UuidType = 'Light'
                UtilUuid.add_uuid(p_pyhouse_obj, l_uuid_obj)
                LOG.info('Loaded light {}'.format(l_obj.Name))
                l_count += 1
        except AttributeError as e_err:  # No Lights section
            LOG.warning('Lighting_Lights - No Lights defined - {}'.format(e_err))
            #  print('XXX-1', e_err)
            l_dict = {}
        LOG.info("Loaded {} Lights".format(l_count))
        return l_dict

    @staticmethod
    def write_all_GarageDoors_xml(p_pyhouse_obj):
        l_xml = ET.Element('GarageDoorSection')
        l_count = 0
        for l_light_obj in p_pyhouse_obj.House.Lighting.Lights.itervalues():
            l_one = Utility._write_one_light_xml(p_pyhouse_obj, l_light_obj)
            l_xml.append(l_one)
            l_count += 1
        LOG.info('Saved {} Lights XML'.format(l_count))
        return l_xml

# ## END DBK
