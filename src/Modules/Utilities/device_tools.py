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


class XmlConfigTools(object):

    def read_base_device_object_xml(self, p_base_obj, p_entry_element_xml):
        """
        Get the BaseObject entries from the XML element.

        Note that a UUID will be generated if one does not exist.

        @param p_base_obj: is the object into which we will put the data.
        @param p_entry_element_xml: is the element we will extract data from (including children).
        """
        l_base_obj = DeviceData()
        try:
            l_base_obj.Name = PutGetXML.get_text_from_xml(p_entry_element_xml, 'Name', 'Missing Name')
            l_base_obj.Key = PutGetXML.get_int_from_xml(p_entry_element_xml, 'Key', 0)
            l_base_obj.Active = PutGetXML.get_bool_from_xml(p_entry_element_xml, 'Active', False)
            l_base_obj.UUID = PutGetXML.get_uuid_from_xml(p_entry_element_xml, 'UUID')
            l_base_obj.Comment = PutGetXML.get_text_from_xml(p_entry_element_xml, 'Comment')
            l_base_obj.DeviceType = PutGetXML.get_int_from_xml(p_entry_element_xml, 'DeviceType')
            l_base_obj.DeviceSubType = PutGetXML.get_int_from_xml(p_entry_element_xml, 'DeviceSubType')
            l_base_obj.DeviceFamily = PutGetXML.get_text_from_xml(p_entry_element_xml, 'DeviceFamily')
            l_base_obj.RoomName = PutGetXML.get_text_from_xml(p_entry_element_xml, 'RoomName')
            l_base_obj.RoomCoords = PutGetXML.get_coords_from_xml(p_entry_element_xml, 'RoomCoords')
        except Exception as e_err:
            print('ERROR in xml_tools.read_base_obj_xml() - {}'.format(e_err))
        return l_base_obj

    def write_base_object_xml(self, p_element_name, p_object):
        """
        Note that UUID is optional.
        """
        l_elem = ET.Element(p_element_name)
        PutGetXML.put_text_attribute(l_elem, 'Name', p_object.Name)
        PutGetXML.put_int_attribute(l_elem, 'Key', p_object.Key)
        PutGetXML.put_bool_attribute(l_elem, 'Active', p_object.Active)
        try:
            PutGetXML.put_uuid_element(l_elem, 'UUID', p_object.UUID)
        except AttributeError:
            PutGetXML.put_uuid_element(l_elem, 'UUID', 'No UUID Given')
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
