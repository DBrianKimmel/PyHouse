"""
-*- test-case-name: PyHouse.src.Modules.Utilities.test.test_device_tools -*-

@name:      PyHouse/src/Modules/Utilities/device_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 26, 2015
@Summary:   Routines to load and save basic Device Data

"""


# Import system type stuff
from xml.etree import ElementTree as ET

# Import PyHouse files
from Modules.Utilities.xml_tools import PutGetXML
from Modules.Core.data_objects import DeviceData
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.DeviceTools    ')


class XML(object):

    @staticmethod
    def read_base_device_object_xml(p_entry_element_xml):
        """
        Get the BaseObject entries from the XML element.
        @param p_entry_element_xml: is the element we will extract data from (including children).
        """
        l_obj = DeviceData()
        try:
            l_obj.Name = PutGetXML.get_text_from_xml(p_entry_element_xml, 'Name', 'Missing Name')
            l_obj.Key = PutGetXML.get_int_from_xml(p_entry_element_xml, 'Key', 0)
            l_obj.Active = PutGetXML.get_bool_from_xml(p_entry_element_xml, 'Active', False)
            l_obj.UUID = PutGetXML.get_uuid_from_xml(p_entry_element_xml, 'UUID')
            l_obj.Comment = PutGetXML.get_text_from_xml(p_entry_element_xml, 'Comment')
            l_obj.DeviceType = PutGetXML.get_int_from_xml(p_entry_element_xml, 'DeviceType')
            l_obj.DeviceSubType = PutGetXML.get_int_from_xml(p_entry_element_xml, 'DeviceSubType')
            l_obj.DeviceFamily = PutGetXML.get_text_from_xml(p_entry_element_xml, 'DeviceFamily')
            l_obj.RoomName = PutGetXML.get_text_from_xml(p_entry_element_xml, 'RoomName')
            l_obj.RoomCoords = PutGetXML.get_coords_from_xml(p_entry_element_xml, 'RoomCoords')
        except Exception as e_err:
            LOG.warn('ERROR in xml_tools.read_base_obj_xml() - {}'.format(e_err))
        return l_obj

    @staticmethod
    def write_base_device_object_xml(p_element_name, p_obj):
        """
        @param p_element_name: is the element name that we are going to create.
        @param p_obj: is the object that contains the device data for which we will output the XML
        @return: the XML element with children that we will create.
        """
        l_elem = ET.Element(p_element_name)
        PutGetXML.put_text_attribute(l_elem, 'Name', p_obj.Name)
        PutGetXML.put_int_attribute(l_elem, 'Key', p_obj.Key)
        PutGetXML.put_bool_attribute(l_elem, 'Active', p_obj.Active)
        # add sub elements
        try:
            PutGetXML.put_uuid_element(l_elem, 'UUID', p_obj.UUID)
        except AttributeError:
            PutGetXML.put_uuid_element(l_elem, 'UUID', 'No UUID Given')
        PutGetXML.put_text_element(l_elem, 'Comment', p_obj.Comment)
        PutGetXML.put_int_element(l_elem, 'DeviceType', p_obj.DeviceType)
        PutGetXML.put_int_element(l_elem, 'DeviceSubType', p_obj.DeviceSubType)
        PutGetXML.put_text_element(l_elem, 'DeviceFamily', p_obj.DeviceFamily)
        PutGetXML.put_text_element(l_elem, 'RoomName', p_obj.RoomName)
        PutGetXML.put_coords_element(l_elem, 'RoomCoords', p_obj.RoomCoords)
        return l_elem

def stuff_new_attrs(p_target_obj, p_data_obj):
    """Put the NEW information from the data object into the target object.
    Preserve any attributes already in the target object.
    Skip system '__' and private '_' attributes
    """
    l_attrs = filter(lambda aname: not aname.startswith('_'), dir(p_data_obj))
    for l_attr in l_attrs:
        if not hasattr(p_target_obj, l_attr):
            setattr(p_target_obj, l_attr, getattr(p_data_obj, l_attr))

# ## END DBK
