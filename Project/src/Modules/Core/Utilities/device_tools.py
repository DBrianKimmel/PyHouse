"""
@name:      Modules/Core/Utilities/device_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 26, 2015
@Summary:   Routines to load and save basic Device Data

"""

__updated__ = '2019-07-31'

#  Import system type stuff

#  Import PyHouse files
from Modules.House import utils
from Modules.Core.Utilities.xml_tools import PutGetXML, XmlConfigTools
from Modules.Core import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.DeviceTools    ')


class XML(object):

    @staticmethod
    def read_base_device_object_xml(p_obj, p_xml):
        """
        Get the BaseUUIDObject entries from the XML element.
        Adds: Device Info, Room Info.

        @param p_obj: is the object we wish to populate with data
        @param p_xml: is the element we will extract data from (including children).
        """
        XmlConfigTools.read_base_UUID_object_xml(p_obj, p_xml)
        try:
            # p_obj.Comment = PutGetXML.get_text_from_xml(p_xml, 'Comment')
            p_obj.DeviceFamily = PutGetXML.get_text_from_xml(p_xml, 'DeviceFamily')
            p_obj.DeviceType = PutGetXML.get_text_from_xml(p_xml, 'DeviceType')
            p_obj.DeviceSubType = PutGetXML.get_text_from_xml(p_xml, 'DeviceSubType')
            utils.read_room_reference_xml(p_obj, p_xml)
        except Exception as e_err:
            LOG.error('ERROR in xml_tools.read_base_obj_xml() - {}'.format(e_err))
        return p_obj

    @staticmethod
    def write_base_device_object_xml(p_element_tag, p_obj):
        """
        @param p_element_tag: is the element name that we are going to create.
        @param p_obj: is the object that contains the device data for which we will output the XML
        @return: the XML element with children that we will create.
        """
        l_elem = XmlConfigTools.write_base_UUID_object_xml(p_element_tag, p_obj)
        PutGetXML.put_text_element(l_elem, 'DeviceFamily', p_obj.DeviceFamily)
        PutGetXML.put_text_element(l_elem, 'DeviceType', p_obj.DeviceType)
        PutGetXML.put_text_element(l_elem, 'DeviceSubType', p_obj.DeviceSubType)
        PutGetXML.put_coords_element(l_elem, 'RoomCoords', p_obj.RoomCoords)
        PutGetXML.put_text_element(l_elem, 'RoomName', p_obj.RoomName)
        PutGetXML.put_text_element(l_elem, 'RoomUUID', p_obj.RoomUUID)
        return l_elem

#  ## END DBK
