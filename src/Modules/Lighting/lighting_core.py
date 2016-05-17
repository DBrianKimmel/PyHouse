"""
-*- test-case-name: PyHouse.Modules.Lighting.test.test_lighting_core -*-

@name:      PyHouse/src/Modules/Lighting/lighting_core.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@note:      Created on Jun 13, 2013
@license:   MIT License
@summary:   A base class for all things lighting

This is for lighting type devices.

Lighting devices are a compound entry in the XML config file.
It is compound since a controller will contain Light entries, controller entries, interface entries etc.
"""

#  Import system type stuff
from distutils.version import LooseVersion

#  Import PyHouse files
from Modules.Utilities.device_tools import XML as deviceXML
from Modules.Utilities.xml_tools import PutGetXML, XmlConfigTools
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.LightingCore   ')


class API(object):

    @staticmethod
    def _read_device_v1_3(p_device_obj, p_entry_xml):
        """
        Read the XML file version 1.3 - convert to 1.4
        """
        p_device_obj.Comment = ''
        p_device_obj.DeviceFamily = PutGetXML.get_text_from_xml(p_entry_xml, 'ControllerFamily')
        p_device_obj.DeviceType = 1
        p_device_obj.DeviceSubType = 0
        p_device_obj.LightingType = PutGetXML.get_text_from_xml(p_entry_xml, 'LightingType')
        p_device_obj.RoomCoords = PutGetXML.get_coords_from_xml(p_entry_xml, 'Coords')
        p_device_obj.RoomName = PutGetXML.get_text_from_xml(p_entry_xml, 'RoomName')
        return p_device_obj

    @staticmethod
    def _read_device_latest(p_device_obj, p_entry_xml):
        """
        """
        p_device_obj.Comment = PutGetXML.get_text_from_xml(p_entry_xml, 'Comment')
        p_device_obj.DeviceFamily = PutGetXML.get_text_from_xml(p_entry_xml, 'DeviceFamily')
        p_device_obj.DeviceType = PutGetXML.get_int_from_xml(p_entry_xml, 'DeviceType')
        p_device_obj.DeviceSubType = PutGetXML.get_int_from_xml(p_entry_xml, 'DeviceSubType')
        p_device_obj.LightingType = PutGetXML.get_text_from_xml(p_entry_xml, 'LightingType')
        p_device_obj.RoomCoords = PutGetXML.get_coords_from_xml(p_entry_xml, 'RoomCoords')
        p_device_obj.RoomName = PutGetXML.get_text_from_xml(p_entry_xml, 'RoomName')
        return p_device_obj

    @staticmethod
    def _read_versioned_device(p_pyhouse_obj, p_device_obj, p_entry_xml):
        return API._read_device_latest(p_device_obj, p_entry_xml)

    @staticmethod
    def _read_base(p_pyhouse_obj, p_device_obj, p_entry_xml):
        deviceXML.read_base_device_object_xml(p_pyhouse_obj, p_device_obj, p_entry_xml)
        return p_device_obj  #  for testing

    @staticmethod
    def read_core_lighting_xml(p_pyhouse_obj, p_device_obj, p_entry_xml):
        """
        This will read some of the lighting information (Core) from a "Lighting" type device.
        @param p_device_obj: is the device we are extracting information for
                we pass this in because it is different for various device types.
        @param p_entry_xml: is the lighting type device XML element
        @param p_version: is some helper data to get the correct information from the config file.
        @return: a dict of the entry to be attached to a higher object.
        """
        API._read_base(p_pyhouse_obj, p_device_obj, p_entry_xml)
        API._read_versioned_device(p_pyhouse_obj, p_device_obj, p_entry_xml)
        return p_device_obj


    @staticmethod
    def write_core_lighting_xml(p_element_tag, p_device_obj):
        """
        @param p_element_tag: is the tag/name of the element that will be created
        @param p_device_obj: is the device object that holds the device information.
        @return: the XML element for the device with some sub-elements already attached.
        """
        l_xml = deviceXML.write_base_device_object_xml(p_element_tag, p_device_obj)
        return l_xml

#  ## END DBK
