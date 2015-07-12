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

# Import system type stuff

# Import PyHouse files
from Modules.Utilities.xml_tools import PutGetXML, XmlConfigTools
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.LightingCore   ')


class LightingCoreXmlAPI(object):

    def _read_base_v1_3(self, p_device_obj, p_entry_xml):
        """
        Read the XML file version 1.3
        """
        p_device_obj.DeviceFamily = PutGetXML.get_text_from_xml(p_entry_xml, 'ControllerFamily')
        p_device_obj.LightingType = PutGetXML.get_text_from_xml(p_entry_xml, 'LightingType')
        p_device_obj.RoomCoords = PutGetXML.get_text_from_xml(p_entry_xml, 'Coords')
        return p_device_obj

    def _read_base_latest(self, p_device_obj, p_entry_xml):
        """
        Read the config file version 1.4.0
        """
        p_device_obj.Comment = PutGetXML.get_text_from_xml(p_entry_xml, 'Comment')
        p_device_obj.LightingType = PutGetXML.get_text_from_xml(p_entry_xml, 'LightingType')
        p_device_obj.RoomName = PutGetXML.get_text_from_xml(p_entry_xml, 'RoomName')
        p_device_obj.RoomCoords = PutGetXML.get_coords_from_xml(p_entry_xml, 'RoomCoords')
        if p_device_obj.RoomCoords == None:
            p_device_obj.RoomCoords = PutGetXML.get_coords_from_xml(p_entry_xml, 'Coords')
        l_tmp = PutGetXML.get_text_from_xml(p_entry_xml, 'DeviceFamily')
        p_device_obj.DeviceFamily = l_tmp
        if p_device_obj.DeviceFamily == 'None':
            p_device_obj.DeviceFamily = PutGetXML.get_text_from_xml(p_entry_xml, 'ControllerFamily')
        return p_device_obj

    def read_core_lighting_xml(self, p_device_obj, p_entry_xml):
        """
        This will read some of the lighting information from a "Lighting" type device.
        @param p_device_obj: is the device we are extracting information for.
        @param p_entry_xml: is the lighting type device XML element
        @return: a dict of the entry to be attached to a higher object.
        """
        XmlConfigTools.read_base_object_xml(p_device_obj, p_entry_xml)
        self._read_base_latest(p_device_obj, p_entry_xml)
        p_device_obj.DeviceType = 1
        return p_device_obj


    def write_base_lighting_xml(self, p_element_tag, p_device_obj):
        """
        @param p_element_tag: is the tag/name of the element that will be created
        @param p_device_obj: is the device object that holds the device information.
        @return: the XML element for the device with some sub-elements already attached.
        """
        l_xml = XmlConfigTools().write_base_object_xml(p_element_tag, p_device_obj)
        PutGetXML.put_text_element(l_xml, 'Comment', p_device_obj.Comment)
        PutGetXML.put_text_element(l_xml, 'DeviceFamily', p_device_obj.DeviceFamily)
        PutGetXML.put_int_element(l_xml, 'DeviceType', p_device_obj.DeviceType)
        PutGetXML.put_int_element(l_xml, 'DeviceSubType', p_device_obj.DeviceSubType)
        PutGetXML.put_text_element(l_xml, 'LightingType', p_device_obj.LightingType)
        PutGetXML.put_coords_element(l_xml, 'RoomCoords', p_device_obj.RoomCoords)
        PutGetXML.put_text_element(l_xml, 'RoomName', p_device_obj.RoomName)
        return l_xml

# ## END DBK
